#!/usr/bin/env python3
import os
import sys
import gzip

# Input: fna files from GTDB (i.e. ssu_r89.fna from GTDBr89)
filename_fna = sys.argv[1]

seq_list = dict()
f_fna = open(filename_fna, 'r')
if filename_fna.endswith('.gz'):
    f_fna = gzip.open(filename_fna, 'rt')

filename_out = os.path.basename(filename_fna).split('.')[0]
filename_out = 'GTDB_%s.v1' % (filename_out)

for line in f_fna:
    if line.startswith('>'):
        tmp_h = line.strip().lstrip('>')
        tmp_id = tmp_h.split()[0]
        tmp_sp_name = tmp_h.split(';')[-1].split('[')[0].strip()
        tmp_sp_name = tmp_sp_name.replace('s__', '')
        tmp_sp_name = tmp_sp_name.replace(' ', '_')

        tmp_h = "%s|%s" % (tmp_sp_name, tmp_id)
        seq_list[tmp_h] = []
    else:
        seq_list[tmp_h].append(line.strip())
f_fna.close()

# Set the sequence length criteria based on the mode.
mode_len = 1537
min_len = mode_len - 40
max_len = mode_len + 40

count_total = 0
count_filtered = 0

f_out = open('%s.fa' % filename_out, 'w')
f_log = open('%s.log' % filename_out, 'w')
for tmp_h in sorted(seq_list.keys()):
    tmp_seq = ''.join(seq_list[tmp_h])
    count_total += 1

    if len(tmp_seq) < min_len:
        count_filtered += 1
        f_log.write('#Filtered: %s (len=%d)\n' % (tmp_h, len(tmp_seq)))
        continue

    if len(tmp_seq) > max_len:
        count_filtered += 1
        f_log.write('#Filtered: %s (len=%d)\n' % (tmp_h, len(tmp_seq)))
        continue

    f_out.write(">%s\n%s\n" % (tmp_h, tmp_seq))
f_out.close()

f_log.write('#Total count: %d\n' % count_total)
pct_filtered = count_filtered * 100.0 / count_total
f_log.write('#Filtered: %d (%.2f pct)\n' % (count_filtered, pct_filtered))
f_log.write('#Filtered min len: %d\n' % min_len)
f_log.write('#Filtered max len: %d\n' % max_len)

f_log.close()
f_out.close()
