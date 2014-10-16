#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
print "Content-type: text/html\n\n";
print 	
'<html>
 <head> 
 <title>LOVE2041</title> 
 <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"     rel="stylesheet">
 </head>
';

$homePage = param('home_page'); 
$browsePage = param('browse_page'); 
$profilePage = param('profile_page'); 

if (defined $homePage) { 
    print 'Welcome to LOVE2041';
    print renderBrowsePage();
} elsif (defined $browsePage) { 
    print 'Browse Page';
    print renderHomePage();
} elsif (defined $profilePage) { 
    print 'Profile Page';
} else { 
    print 'Welcome to LOVE2041';
    print renderBrowsePage();
}
print '</html>';

sub renderHomePage { 
    param('home_page', 'true');
    return
        start_form,
        hidden ('home_page', $homePage), 
        submit('Back To Home!'),  
        end_form, 
}

sub renderBrowsePage { 
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        submit('Begin!'),  
        end_form, 
}

