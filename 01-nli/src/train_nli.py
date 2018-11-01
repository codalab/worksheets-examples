# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from __future__ import print_function
import os
import sys
import time
import json
import argparse
import numpy as np

import torch
from torch.autograd import Variable
import torch.nn as nn

from data import get_nli, get_batch, build_vocab
from mutils import get_optimizer
from models import NLINet
from run_info import RunInfo

parser = argparse.ArgumentParser(description='NLI training')
# paths
parser.add_argument("--nlipath", type=str, default='datasets/SNLI/', help="SNLI data path")
parser.add_argument("--outputdir", type=str, default='experiments/', help="output directory")
parser.add_argument("--outputmodelname", type=str, default='model.pickle')
parser.add_argument("--word_emb_path", type=str, default="datasets/GloVe/glove.840B.300d.txt", help="word embedding file path")

# training
parser.add_argument("--n_epochs", type=int, default=20)
parser.add_argument("--batch_size", type=int, default=64)
parser.add_argument("--dpout_model", type=float, default=0., help="encoder dropout")
parser.add_argument("--dpout_fc", type=float, default=0., help="classifier dropout")
parser.add_argument("--nonlinear_fc", type=float, default=0, help="use nonlinearity in fc")
parser.add_argument("--optimizer", type=str, default="sgd,lr=0.1", help="adam or sgd,lr=0.1")
parser.add_argument("--lrshrink", type=float, default=5, help="shrink factor for sgd")
parser.add_argument("--decay", type=float, default=0.99, help="lr decay")
parser.add_argument("--minlr", type=float, default=1e-5, help="minimum lr")
parser.add_argument("--max_norm", type=float, default=5., help="max norm (grad clipping)")
parser.add_argument("--train_frac", type=float, default=1., help="fraction of training data to use")

# model
parser.add_argument("--encoder_type", type=str, default='InferSent', help="see list of encoders")
parser.add_argument("--enc_lstm_dim", type=int, default=256, help="encoder nhid dimension")
parser.add_argument("--n_enc_layers", type=int, default=1, help="encoder num layers")
parser.add_argument("--fc_dim", type=int, default=128, help="nhid of fc layers")
parser.add_argument("--n_classes", type=int, default=3, help="entailment/neutral/contradiction")
parser.add_argument("--pool_type", type=str, default='max', help="max or mean")

# gpu
parser.add_argument("--gpu_id", type=int, default=0, help="GPU ID")
parser.add_argument("--seed", type=int, default=1234, help="seed")

# data
parser.add_argument("--word_emb_dim", type=int, default=300, help="word embedding dimension")

params, _ = parser.parse_known_args()
run_info = RunInfo(params.outputdir)

# Write out command-line arguments
run_info.write_args(params)

# set gpu device
USE_CUDA = torch.cuda.is_available()
DEVICE = torch.device("cuda" if USE_CUDA else "cpu")
if USE_CUDA: torch.cuda.set_device(params.gpu_id)
print('using cuda:\n', USE_CUDA, '\n')

# print parameters
print('parameters (passed):\n', '{0}'.format(sys.argv[1:]), '\n')
print('parameters (all):\n', params, '\n')

"""
SEED
"""
np.random.seed(params.seed)
torch.manual_seed(params.seed)
torch.cuda.manual_seed(params.seed)

"""
DATA
"""
train, dev, test = get_nli(params.nlipath, use_frac={'train': params.train_frac})
word_vec = build_vocab(train['s1'] + train['s2'] +
                       dev['s1'] + dev['s2'] +
                       test['s1'] + test['s2'], params.word_emb_path)

for split in ['s1', 's2']:
    for data_type in ['train', 'dev', 'test']:
        eval(data_type)[split] = np.array([['<s>'] +
            [word for word in sent.split() if word in word_vec] +
            ['</s>'] for sent in eval(data_type)[split]])


"""
MODEL
"""
# model config
config_nli_model = {
    'n_words'        :  len(word_vec)         ,
    'word_emb_dim'   :  params.word_emb_dim   ,
    'enc_lstm_dim'   :  params.enc_lstm_dim   ,
    'n_enc_layers'   :  params.n_enc_layers   ,
    'dpout_model'    :  params.dpout_model    ,
    'dpout_fc'       :  params.dpout_fc       ,
    'fc_dim'         :  params.fc_dim         ,
    'bsize'          :  params.batch_size     ,
    'n_classes'      :  params.n_classes      ,
    'pool_type'      :  params.pool_type      ,
    'nonlinear_fc'   :  params.nonlinear_fc   ,
    'encoder_type'   :  params.encoder_type   ,
    'use_cuda'       :  USE_CUDA              ,
}

# model
encoder_types = ['InferSent', 'BLSTMprojEncoder', 'BGRUlastEncoder',
                 'InnerAttentionMILAEncoder', 'InnerAttentionYANGEncoder',
                 'InnerAttentionNAACLEncoder', 'ConvNetEncoder', 'LSTMEncoder']
assert params.encoder_type in encoder_types, "encoder_type must be in " + \
                                             str(encoder_types)
nli_net = NLINet(config_nli_model)
print('\nmodel:\n', nli_net, '\n')

# loss
weight = torch.FloatTensor(params.n_classes).fill_(1)
loss_fn = nn.CrossEntropyLoss(weight=weight)
loss_fn.size_average = False

# optimizer
optim_fn, optim_params = get_optimizer(params.optimizer)
optimizer = optim_fn(nli_net.parameters(), **optim_params)

# cuda, if available
nli_net.to(DEVICE)
loss_fn.to(DEVICE)


"""
TRAIN
"""
val_acc_best = -1e10
adam_stop = False
stop_training = False
lr = optim_params['lr'] if 'sgd' in params.optimizer else None

def train_epoch(epoch, log):
    run_info.update_stats({'epoch': epoch})

    print('\nTRAINING : Epoch ' + str(epoch))
    nli_net.train()
    all_costs = []
    words_count = 0

    last_time = time.time()
    correct = 0.

    # shuffle the data
    permutation = np.random.permutation(len(train['s1']))
    s1 = train['s1'][permutation]
    s2 = train['s2'][permutation]
    target = train['label'][permutation]

    optimizer.param_groups[0]['lr'] = optimizer.param_groups[0]['lr'] * params.decay if epoch>1\
        and 'sgd' in params.optimizer else optimizer.param_groups[0]['lr']
    print('Learning rate : {0}'.format(optimizer.param_groups[0]['lr']))

    for stidx in range(0, len(s1), params.batch_size):
        # prepare batch
        s1_batch, s1_len = get_batch(s1[stidx:stidx + params.batch_size],
                                     word_vec, params.word_emb_dim)
        s2_batch, s2_len = get_batch(s2[stidx:stidx + params.batch_size],
                                     word_vec, params.word_emb_dim)
        s1_batch, s2_batch = Variable(s1_batch.to(DEVICE)), Variable(s2_batch.to(DEVICE))
        tgt_batch = Variable(torch.LongTensor(target[stidx:stidx + params.batch_size])).to(DEVICE)
        k = s1_batch.size(1)  # actual batch size

        # model forward
        output = nli_net((s1_batch, s1_len), (s2_batch, s2_len))

        pred = output.data.max(1)[1]
        correct += pred.long().eq(tgt_batch.data.long()).cpu().sum()
        assert len(pred) == len(s1[stidx:stidx + params.batch_size])

        # loss
        loss = loss_fn(output, tgt_batch)
        all_costs.append(loss.data.item())
        words_count += (s1_batch.nelement() + s2_batch.nelement()) / params.word_emb_dim

        # backward
        optimizer.zero_grad()
        loss.backward()

        # gradient clipping (off by default)
        shrink_factor = 1
        total_norm = 0

        for p in nli_net.parameters():
            if p.requires_grad:
                p.grad.data.div_(k)  # divide by the actual batch size
                total_norm += p.grad.data.norm() ** 2
        total_norm = np.sqrt(total_norm)

        if total_norm > params.max_norm:
            shrink_factor = params.max_norm / total_norm
        current_lr = optimizer.param_groups[0]['lr'] # current lr (no external "lr", for adam)
        optimizer.param_groups[0]['lr'] = current_lr * shrink_factor # just for update

        # optimizer step
        optimizer.step()
        optimizer.param_groups[0]['lr'] = current_lr

        if len(all_costs) == 100:
            loss = np.mean(all_costs)
            sentences_per_second = len(all_costs) * params.batch_size / (time.time() - last_time)
            words_per_second = words_count * 1.0 / (time.time() - last_time)
            train_accuracy = float(100.*correct/(stidx+k))

            # Write out statistics
            stats = {
                'example': stidx,
                'loss': loss,
                'sentences_per_second': sentences_per_second,
                'words_per_second': words_per_second,
                'train_accuracy': train_accuracy,
                'epoch': epoch,
            }
            print('example {0:d} ; loss {1:4.2f} ; sentence/s {2:3.1f} ; words/s {3:3.1f} ; accuracy train : {4:4.2f}'.format(
                stats['example'],
                stats['loss'],
                stats['sentences_per_second'],
                stats['words_per_second'],
                stats['train_accuracy'],
            ))
            run_info.update_stats(stats)

            log.append(stats)
            run_info.update_log({
                'log': log,
            })

            last_time = time.time()
            words_count = 0
            all_costs = []
    train_acc = 100. * float(correct)/len(s1)
    print('results : epoch {0} ; mean accuracy train : {1:4.2f}'
          .format(epoch, train_acc))
    assert isinstance(train_acc, float)
    return train_acc, log


def evaluate(epoch, eval_type='dev', final_eval=False):
    nli_net.eval()
    correct = 0.
    global val_acc_best, lr, stop_training, adam_stop

    if eval_type == 'dev' and not final_eval:
        print('\nVALIDATION : Epoch {0}'.format(epoch))

    s1 = dev['s1'] if eval_type == 'dev' else test['s1']
    s2 = dev['s2'] if eval_type == 'dev' else test['s2']
    target = dev['label'] if eval_type == 'dev' else test['label']

    for i in range(0, len(s1), params.batch_size):
        # prepare batch
        s1_batch, s1_len = get_batch(s1[i:i + params.batch_size], word_vec, params.word_emb_dim)
        s2_batch, s2_len = get_batch(s2[i:i + params.batch_size], word_vec, params.word_emb_dim)
        s1_batch, s2_batch = Variable(s1_batch.to(DEVICE)), Variable(s2_batch.to(DEVICE))
        tgt_batch = Variable(torch.LongTensor(target[i:i + params.batch_size])).to(DEVICE)

        # model forward
        output = nli_net((s1_batch, s1_len), (s2_batch, s2_len))

        pred = output.data.max(1)[1]
        correct += pred.long().eq(tgt_batch.data.long()).cpu().sum()

    # save model
    eval_acc = 100 * float(correct) / len(s1)
    if final_eval:
        print('finalgrep : accuracy {0} : {1:4.2f}%'.format(eval_type, eval_acc))
    else:
        print('togrep : results : epoch {0} ; mean accuracy {1} : {2:4.2f}'.format(epoch, eval_type, eval_acc))

    if eval_type == 'dev' and epoch <= params.n_epochs:
        if eval_acc > val_acc_best:
            print('saving model at epoch {0}'.format(epoch))
            if not os.path.exists(params.outputdir):
                os.makedirs(params.outputdir)
            torch.save(nli_net.state_dict(), os.path.join(params.outputdir,
                       params.outputmodelname))
            val_acc_best = eval_acc
        else:
            if 'sgd' in params.optimizer:
                optimizer.param_groups[0]['lr'] = optimizer.param_groups[0]['lr'] / params.lrshrink
                print('Shrinking lr by : {0}. New lr = {1}'
                      .format(params.lrshrink,
                              optimizer.param_groups[0]['lr']))
                if optimizer.param_groups[0]['lr'] < params.minlr:
                    stop_training = True
            if 'adam' in params.optimizer:
                # early stopping (at 2nd decrease in accuracy)
                stop_training = adam_stop
                adam_stop = True
    assert isinstance(eval_acc, float)
    return eval_acc


"""
Train model on Natural Language Inference task
"""
epoch = 0
train_acc = 0
log = []
while not stop_training and epoch < params.n_epochs:
    epoch += 1
    train_acc, log = train_epoch(epoch, log)
    evaluate(epoch, 'dev')

# Run best model on test set.
nli_net.load_state_dict(torch.load(os.path.join(params.outputdir, params.outputmodelname)))

print('\nTEST : Epoch {0}'.format(epoch))
dev_acc = evaluate(0, 'dev', True)
test_acc = evaluate(0, 'test', True)
run_info.update_stats({
    'dev_accuracy': dev_acc,
    'test_accuracy': test_acc,
})

# Save encoder instead of full model
torch.save(nli_net.encoder.state_dict(), os.path.join(params.outputdir, params.outputmodelname + '.encoder.pkl'))
