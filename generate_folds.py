from sklearn.cross_validation import StratifiedKFold
import sys
import os

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("this program creates stratified k folds for a jamendo_ds metafile")
        print("usage: %s metafile k [prefix]" % (sys.argv[0]))
        exit(1)
    
    meta_filename = sys.argv[1]
    k = sys.argv[2]
    prefix = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(os.path.splitext(meta_filename)[0])

    with open(meta_filename) as f:
        content = f.readlines()

    labels = [i.split("\t")[1].strip() for i in content]

    folds = StratifiedKFold(labels, n_folds=10, shuffle=True)

    fold = 1
    for train_index, test_index in folds:
        f = open( '%s_f%d_train.txt' % (prefix, fold), 'w')
        for i in train_index:
            f.write(content[i])
        f.close()

        f = open('%s_f%d_evaluate.txt' % (prefix, fold), 'w')
        for i in test_index:
            f.write(content[i])
        f.close()

        f = open('%s_f%d_test.txt' % (prefix, fold), 'w')
        for i in test_index:
            f.write('%s\n' % content[i].split('\t')[0])
        f.close()
        fold+=1
