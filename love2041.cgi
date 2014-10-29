#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Cookie;

use POSIX;
use DateTime;

require "page_browse.cgi";
require "page_profile.cgi";
require "page_register.cgi";
require "page_dashboard.cgi";
require "page_home.cgi";
require "page_match.cgi";



$login = param('login');
$password = param('password');
$directory = "./students";
$browsePage = param('browse_page'); 
$profilePage = param('profile_page');
$searchTerm = param('search_term');
$registerPage = param('register_page');
$viewPerson = param('view_person');
$logout = param('logout_page');
$myProfile = param('my_page');
$myEdit = param('edit_page');
$matchPage = param('match_page');
$dashboardPage = param('my_dashboard');
$registerPage = param('register_page');
$completeReg = param('complete_registration');
$pageNumber = param('page') || 0; 
$edited = param('edited');
$changeText = param('change_text');

if (defined $logout) { 
    $u = CGI::Cookie->new (
        -name => 'username',
        -value => $login,
        -expires => 'now',
    );

    $p = CGI::Cookie->new (
        -name => 'password',
        -value => $password,
        -expires => 'now',
    );

    print "Set-Cookie: $u\n";
    print "Set-Cookie: $p\n";
    print "Location: love2041.cgi\n\n";
}

if (defined $login && defined $password) {
    $u = CGI::Cookie->new (
        -name => 'username',
        -value => $login,
    );

    $p = CGI::Cookie->new (
        -name => 'password',
        -value => $password,
    );

     print "Set-Cookie: $u\n";
     print "Set-Cookie: $p\n";
     print "Location: love2041.cgi\n\n";
} 

print "Content-type: text/html\n\n";


print start_html (
    -title => "LOVE2041",
    -style => [
        { -src => "//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" },
        { -src => "http://fonts.googleapis.com/css?family=Oswald:400,700,300" },
        { -src => "http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" },
        { -src => "css/custom.css" },
    ],
    -script => [ 
        { -src => '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' },
        { -src => 'js/custom.js' },
    ],
);

storeData();

if (authenticate() && !$logout) { 
    if (defined $browsePage || defined $searchTerm) { 
        browsePageHeader();
        browsePageContent();
    } elsif (defined $dashboardPage) { 
        browsePageHeader();
        dashboard();
    } elsif (defined $profilePage) { 
        browsePageHeader();
        printProfile($viewPerson);
    } elsif (defined $myProfile) { 
        browsePageHeader();
        printProfile($login);
    } elsif (defined $myEdit) { 
        browsePageHeader();
        editProfile(); 
    } elsif (defined $matchPage) { 
        browsePageHeader();
        if (defined $matched) { 
            createMatch();
        } else { 
            matchPage();
        }
    } elsif (defined $changeText) { 
        browsePageHeader();
        changeProfile();
        dashboard();
    } else { 
        browsePageHeader();
        dashboard();

    } 
} elsif (defined $registerPage) { 
    registerPage();
} elsif (defined $completeReg) { 
    if (authRegistration()) { 
        confirmRegistration();
    } 
} else {
    homePage();
}

print '</html>';

sub convertAge { 
    $birth = $_[0];
    @birthArray = split ("\/", $birth);
    $date = DateTime->today; 
    $current = $date->date;
    @currentArray = split ("\-", $current);
    $age = $currentArray[0] - $birthArray[0];
    return $age;
}

sub storeData { 
    @people = glob ("$directory/*");
    open (FILE, '>username.txt');
    foreach $people (@people) { 
        $user = getUsername($people);
        $user =~ s/ //g;
        @text = getProfile($user);
        $count = 0; 
        foreach $line (@text) { 
            $count++; 
            if ($line =~ /password:/) { 
                $pass = @text[$count]; 
                $pass =~ s/ +//g;
                print FILE "$user $pass\n";
            }
        }
    }
}

sub authenticate {
    @people = glob ("$directory/*");
    %cookies = CGI::Cookie->fetch;
    if (exists $cookies{'username'}) {
        $password = $cookies{'password'}->value;
        $login = $cookies{'username'}->value;
        foreach $people (@people) { 
            $person = getUsername($people);
            if ($person eq $login) {
                @text = getProfile(getUsername($people));
                $count = 0; 
                foreach $line (@text) { 
                    $count++; 
                    if ($line =~ /password:/) { 
                        $pass = @text[$count]; 
                        return ($pass == $password);
                    }
                }
            }
        } 
    }
    return 0; 
}

sub getUsername { 
    $person = $_[0]; 
    $person =~ s/\.\///g;
    $person =~ s/students\///;
    param('person', $person); 
    return $person;
}

sub getProfile { 
    $person = $_[0]; 
    $n = "$person/profile.txt";
    open $profile, "students/$n" or die;
    $profile = join ('', <$profile>);
    @text = split ("\n", $profile);
    return @text; 
}

sub getPreferences { 
    $person = $_[0]; 
    $n = "$person/preferences.txt";
    open $profile, "students/$n" or die;
    $profile = join ('', <$profile>);
    @text = split ("\n", $profile);
    return @text; 
}
