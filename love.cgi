#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2013
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;

my $html; 
my $directory; 
my $number;
my @people; 
my @gallery;
my @image;
my $filename; 
my $name;
my $profile;
my $person;
my $person2;
my $image;
my @text;
my $line;



$directory = "./students";
print "Content-type: text/html\n\n";
print "<html>";
print getHeader();
print getNext();
$current = param('current'); 

foreach my $i (0..9) { 
    $person = getCurrent();
    print '<div class="row">';
    print '<div class="container">';
    param('person', $person); 
    print getImage($person); 
    print getInfo(); 
    #print getText($person); 
    print '</div>';
    print '</div>';
    print "</html>";
}
if (defined $current) {
    print getText($current);
}


exit 0;

sub getHeader { 
return
	'<head> 
	<title>LOVE2041</title> 
	<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"    rel="stylesheet">
	</head>
	'
}


sub getCurrent { 
	$number = param('number') || 0; 
	@people = glob ("$directory/*");
	$number = min(max($number, 0), $#people);
	param('number', $number + 1);
	$person = $people[$number];
	return $person;
}

sub getImage { 
	$person = $_[0]; 
	$person =~ s/\.\///g;
	$image = "<img src=\"$person/profile.jpg\">";
	return $image; 
}

sub getText { 
	$person = $_[0]; 
	$name = "$person/profile.txt";
	open $profile, "$name" or die;
	$profile = join ('', <$profile>);
	@text = split ("\n", $profile);
	$html = '';
	foreach $line (@text) { 
		if ($line =~ /:$/) {
			$html .= "<b>$line</b><br>";
		} else { 
			$html .= "$line<br>";
		}
	}
	return $html;
}

sub getNext { 
	return	start_form, "\n",
			hidden('number', $number + 10),"\n",
			submit('Next student'),"\n",
			end_form, "\n",
}


sub getInfo { 
param('current', $person);
    return start_form, 
    hidden ('current', $person),
    submit ('get info'), 
    end_form, 
}



