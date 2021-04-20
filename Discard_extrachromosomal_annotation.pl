#!/usr/bin/perl

# define chromosomes to keep

my %chromosomes = ('NC_000067.6',0,
                  'NC_000068.7',0,
                  'NC_000069.6',0,
                  'NC_000070.6',0,
                  'NC_000071.6',0,
                  'NC_000072.6',0,
                  'NC_000073.6',0,
                  'NC_000074.6',0,
                  'NC_000075.6',0,
                  'NC_000076.6',0,
                  'NC_000077.6',0,
                  'NC_000078.6',0,
                  'NC_000079.6',0,
                  'NC_000080.6',0,
                  'NC_000081.6',0,
                  'NC_000082.6',0,
                  'NC_000083.6',0,
                  'NC_000084.6',0,
                  'NC_000085.6',0,
                  'NC_000086.7',0,
                  'NC_000087.7',0,
);

my %hg_chroms = ('NC_000010.11',0,
'NC_000011.10',0,
'NC_000012.12',0,
'NC_000013.11',0,
'NC_000014.9',0,
'NC_000015.10',0,
'NC_000016.10',0,
'NC_000017.11',0,
'NC_000018.10',0,
'NC_000019.10',0,
'NC_000001.11',0,
'NC_000020.11',0,
'NC_000021.9',0,
'NC_000022.11',0,
'NC_000002.12',0,
'NC_000003.12',0,
'NC_000004.12',0,
'NC_000005.10',0,
'NC_000006.12',0,
'NC_000007.14',0,
'NC_000008.11',0,
'NC_000009.12',0
);

open (INPUT, '<', $ARGV[0]) or die "Can't open file";

for (my $i=0; $i < 7; $i++){$line = <INPUT>; print $line;}
while($line = <INPUT>)
  {
     if(substr($line,0,3) eq '###') {print '###'; last;}
     else {
            @line = split /\s/,$line;
            if(exists($chromosomes{$line[1]}))
               {
                 print $line;
                 $line = <INPUT>;
                 do {print $line; $line = <INPUT>;} until(substr($line,0,2) eq '##');
                 redo;
               }
             else {do {$line = <INPUT>;} until(substr($line,0,2) eq '##'); redo;}
          }
  }
close(INPUT);






