import logging
import os.path
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from gensim.corpora import WikiCorpus

if __name__=='__main__':
    
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(ascime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
#    logger.info("running %s"%' '.join(sys.argv))

    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit()
    print sys.argv[1],sys.argv[2]
    intp = sys.argv[1] 
    outp = sys.argv[2]
    space = ' '
    i =0
    output = open(outp,'w')
    wiki = WikiCorpus(intp,lemmatize=False,dictionary=[])
    for text in wiki.get_texts():
        #print space.join(text)
        output.write(space.join(text)+'\n')
        i=i+1
        if (i%10000 == 0):
            print "Saved "+str(i)+" articles."
    output.close()
