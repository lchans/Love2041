#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Cookie;
use File::Path;
use File::Copy;
use POSIX;
use DateTime;

require "pages/page_browse.cgi";
require "pages/page_profile.cgi";
require "pages/page_register.cgi";
require "pages/page_dashboard.cgi";
require "pages/page_home.cgi";
require "pages/page_match.cgi";
require "pages/page_recover.cgi";

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
$homePage = param('home_page');
$dashboardPage = param('my_dashboard');
$registerPage = param('register_page');
$recoverPage = param('recover_page');
$completeReg = param('complete_registration');
$completeRec = param('complete_recover');
$pageNumber = param('page') || 0; 
$edited = param('edited');
$changeText = param('change_text');


if (defined $login && defined $password || defined $logout) {

    if (defined $logout) {$expires = 'now'};
    if (undef $logout) {$expires = '3d'};

    $u = CGI::Cookie->new (
        -name => 'username',
        -value => $login,
        -expires => $expires,
    );

    $p = CGI::Cookie->new (
        -name => 'password',
        -value => $password,
        -expires => $expires, 
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
        { -src => '//maxcdn.bootstrapcdn.com/bootstrap/3.3.0/js/bootstrap.min.js'},
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
        printProfile($login);
    } else { 
        browsePageHeader();
        printProfile($login);

    } 
} elsif (defined $registerPage) { 
    registerPage();
} elsif (defined $recoverPage) { 
    enterUsername(); 

} elsif (defined $completeRec) { 
    authenticateUsername();
} elsif (defined $completeReg) { 
    if (authRegistration()) { 
        confirmRegistration();
    } 
} elsif (defined $homePage) { 
    homePage();
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
    open (FILE, '>', 'username.txt');
    foreach $people (@people) { 
        $user = getUsername($people);
        $user =~ s/ //g;
        @text = getProfile($user);
        $count = 0; 
        foreach $line (@text) { 
            $count++; 
            if ($line =~ /email:/) { 
                $email = @text[$count];
                $email =~ s/ +//g;
            }
            if ($line =~ /password:/) { 
                $pass = @text[$count]; 
                $pass =~ s/ +//g;
                
            }
        }
        print FILE "$user $pass $email\n";
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


=GET USERNAME 
    - Gets the username from a directory
    - Example: ./students/CoolPrincess80
    - Returns: CoolPrincess80
=cut
sub getUsername { 
    $person = $_[0]; 
    $person =~ s/\.\///g;
    $person =~ s/students\///;
    param('person', $person); 
    return $person;
}

=GET PROFILE 
    - Gets the text from profile.txt from a username
=cut
sub getProfile { 
    $person = $_[0]; 
    $n = "$person/profile.txt";
    open $profile, "students/$n" or die;
    $profile = join ('', <$profile>);
    @text = split ("\n", $profile);
    return @text; 
}

=GET PREFERENCES 
    - Gets the text from preferences.txt from a username
=cut

sub getPreferences { 
    $person = $_[0]; 
    $n = "$person/preferences.txt";
    open $profile, "students/$n" or die;
    $profile = join ('', <$profile>);
    @text = split ("\n", $profile);
    return @text; 
}


=GETHASH
    - Retrieves all the text from a profile and stores it into a hashmap
    - Keys are the section of the title, ie. username: 
    - Values are the information beneath the title, ie. CoolPrincess60
=cut
sub getHash {
    $tabs{'username:'} = ""; 
    $tabs{'name:'} = ""; 
    $tabs{'email:'} = ""; 
    $tabs{'password:'} = ""; 
    $tabs{'gender:'} = "";
    $tabs{'weight:'} = ""; 
    $tabs{'birthdate:'} = ""; 
    $tabs{'hair_colour:'} = "";
    $tabs{'degree:'} = ""; 
    $tabs{'courses:'} = "";
    $tabs{'favourite_bands:'} = ""; 
    $tabs{'favourite_hobbies:'} = "";
    $tabs{'favourite_movies:'} = ""; 
    $tabs{'favourite_books:'} = "";
    $tabs{'favourite_TV_shows:'} = ""; 
    open $profile, "<", "students\/$_[0]\/profile.txt" or die;
    @sub = split ("\n", $profile);
    foreach $line (@sub) { 
        if ($line != /^$/) { 
            if ($line =~ /:/) { 
                $line =~ s/\s//g;
                $header = $line;
            } else {
                $line =~ s/\t//g;
                $tabs{$header} .= "$line<br>\n"; 
            }
        }
    }
    return %tabs;
}
