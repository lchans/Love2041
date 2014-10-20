#!/usr/bin/perl

open(my $file, '>>', 'username.txt') or die;
print $file ("username password\n"); 
