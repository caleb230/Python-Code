#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
#from Bio import Seq
#from Bio.Seq import MutableSeq
#from Bio import SeqIO
#from Bio import Alphabet

def read_fasta_seqs( fileName ):
        seqs = { }
        inputStream = open(fileName,'r')
        for line in inputStream.readlines():
                if line[0] == '>':
                        seqID = line[1:].strip('\r\n')
                        seqs[seqID] = ''
                        continue
                else:
                        seqs[seqID] += line.strip('\r\n')
        return seqs

def read_blat_align( fileName ):
        aln = {}
        fh = open( fileName, 'r' )
        # skip the header rows (first 5 lines)
        for i in range(5):
                fh.readline()
        for line in fh.readlines():
                fields = line.strip('\r\n').split('\t')
                query_id = fields[9]
                if query_id not in aln:
                        aln[query_id] = {}
                aln[query_id]['MATCH_LEN'] = int(fields[0])     
                aln[query_id]['MISMATCH_LEN'] = int(fields[1])
                aln[query_id]['REPMATCH_LEN'] = int(fields[2])  
                aln[query_id]['NUM_N'] = int(fields[3])
                aln[query_id]['NUM_QUERY_GAPS'] = int(fields[4])        
                aln[query_id]['QUERY_GAP_BASES'] = int(fields[5])
                aln[query_id]['NUM_TARG_GAPS'] = int(fields[6])
                aln[query_id]['TARG_GAP_BASES'] = int(fields[7])
                aln[query_id]['STRAND'] = str(fields[8])
                aln[query_id]['QUERY_NAME'] = str(fields[9])
                aln[query_id]['QUERY_LEN'] = int(fields[10])
                aln[query_id]['QUERY_MATCH_START'] = int(fields[11])
                aln[query_id]['QUERY_MATCH_END'] = int(fields[12])
                aln[query_id]['TARG_NAME'] = str(fields[13])
                aln[query_id]['TARG_LEN'] = int(fields[14])
                aln[query_id]['TARG_MATCH_START'] = int(fields[15])
                aln[query_id]['TARG_MATCH_END'] = int(fields[16])
                aln[query_id]['NUM_ALN_BLOCKS'] = int(fields[17])
                aln[query_id]['ALN_BLOCK_SIZES'] = map(int,fields[18].rstrip(',').split(','))
                aln[query_id]['QUERY_ALN_BLOCK_STARTS'] = map(int,fields[19].rstrip(',').split(','))
                aln[query_id]['TARG_ALN_BLOCK_STARTS'] = map(int,fields[20].rstrip(',').split(','))
        fh.close()
        return aln

# function to create the reverse complement of a DNA sequence
def reverse_complement( seq ):
        ndict={'C':'G','A':'T','T':'A','G':'C'}
        comp=''
        for nuc in seq:
         comp+=ndict[nuc]
        rs=[nuc for nuc in reversed(comp)]
        return ''.join(rs)
        

def assemble_gene_sequence(ref_seq, query_seqs, aln):        
        final_seq=''*len(ref_seq.values()[0])            #list to string conversion
        
        for query_id in aln:
                qid_seq=query_seqs[query_id]
                if aln[query_id]['STRAND']=='-':
                        qid_seq=reverse_complement(qid_seq)
                seq_aln=aln[query_id]
                for b in range(aln[query_id]['NUM_ALN_BLOCKS']):              
                        block_size=aln[query_id]['ALN_BLOCK_SIZES'][b]
                        q_block_start=aln[query_id]['QUERY_ALN_BLOCK_STARTS'][b]
                        q_block=qid_seq[q_block_start:q_block_start+block_size]
                        t_block_start=aln[query_id]['TARG_ALN_BLOCK_STARTS'][b]
                        templist=list(final_seq)
                        templist[t_block_start:(t_block_start+block_size)]=list(q_block)    #Only list can be given assignment
                        final_seq=''.join(templist)
               
        return final_seq
                

                    
        
# The main function
ref_seq = read_fasta_seqs( 'refseq9.fa' )
querySeqs = read_fasta_seqs( 'seq9_chopped.fa' )
#for s in tumorSeqs.keys():
#       print ">%s\n%s" % (s,tumorSeqs[s])
Align = read_blat_align( 'output.psl' )

##num_seqs={}for qid in Align:
##        if Align[qid]['TARG_NAME'] not in num_seqs:
##                num_seqs[qid]['TARG_NAME']=1
##        else:
##                num_seqs[qid]['TARG_NAME']+=1
##num_hits=0
##best_targ=''
##for targ in num_seqs:
##        if num_seqs[targ]>num_hits:
##                best_targ=targ
##                num_hits=num_seqs[targ]  
Allele = assemble_gene_sequence( ref_seq, querySeqs, Align )


print '>Allele\n%s' % Allele



