#!/usr/bin/perl
# Note: This is a bastardized version of the rep1 program
# replaces a string within multiple files
# specified on the command line

$mv = '/bin/mv';

$op = shift || die("Usage: $0 perlexpr [filenames]\n");

if (!@ARGV) {
  @ARGV = <STDIN>;
  chop(@ARGV);
}

foreach $file (@ARGV) {
  if (!-f $file) {
       print "Skipping non-regular file: $file\n";
       next;
  }
  if (-B $file) {
       print "Skipping binary file: $file\n";
       next;
  }

  $outfile = "/home/yao/glycomimetic_simulations/scripts/tmp_for_formatAtomNumEsp_pl/$file.$$";

  open(FILE, $file) ||
       die("Couldn't open $file: $!\n");
  undef $/;
  $_ = <FILE>;
  close(FILE);

  if (eval $op) {
    open(OFILE, "> $outfile") ||
        die("Couldn't open $outfile: $!\n");
    print OFILE;
    close(OFILE);

#    system($mv, '-f', $file, "$file.bak");
    system($mv, '-f', $outfile, $file);

    print "File changed: $file\n";
  }
  else {
    print "No change to file: $file\n";
  }
}

exit(0);

