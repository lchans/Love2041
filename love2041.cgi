#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Cookie;

require "page_browse.cgi";
require "page_profile.cgi";

$login = param('login');
$password = param('password');
$directory = "./students";
$homePage = param('home_page'); 
$browsePage = param('browse_page'); 
$profilePage = param('profile_page');
$searchTerm = param('search_term');
$registerPage = param('register_page');
$viewPerson = param('view_person');
$logout = param('logout_page');
$myProfile = param('my_page');
$pageNumber = param('page') || 1; 


if (defined $login && defined $password) {
    my $u = CGI::Cookie->new (
        -name => 'username',
        -value => $login,
    );

    my $p = CGI::Cookie->new (
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
        { -src => "http://fonts.googleapis.com/c`ss?family=Oswald:400,700,300" },
        { -src => "http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" },
        { -src => "custom.css" },
    ]
);

if (authenticate() && !$logout) { 
    if (defined $homePage) { 
        print '<center>';
        print '<h5> LOVE2041</h5>'; 
        loginPage();
        print '</center>';
    } elsif (defined $browsePage || defined $searchTerm) { 
        browsePageHeader();
        browsePageContent();
    } elsif (defined $profilePage) { 
        browsePageHeader();
        profilePage($viewPerson);
    } elsif (defined $myProfile) { 
        browsePageHeader();
        profilePage($login);
    } else { 
        browsePageHeader();
        browsePageContent();
    } 
} elsif (!authenticate()) { 
    logoutPage();
    print "<center>Wrong username or password!</center>";
}  else {
    logoutPage();
}

print '</html>';

sub logoutPage { 
    print qq ~ 
    <center>
    <h5>LOVE2041</h5>
    <form>
        <input type="text" name="login">
        <input type="password" name="password">
        <input type="submit" class="btn btn-default">
    </form>
    </center>
    ~
}

sub authenticate {
    %cookies = CGI::Cookie->fetch;
    $password = $cookies{'password'}->value;
    $login = $cookies{'username'}->value;
    @people = glob ("$directory/*");
    foreach $people (@people) { 
        $person = getUsername($people);
        if ($person eq $login) {
            @text = getProfile(getUsername($people));
            $count = 0; 
            foreach $line (@text) { 
                $count++; 
                if ($line =~ /password:/) { 
                    $pass = @text[$count]; 
                    $pass =~ s/ //g;
                    if ($pass == $password) { 
                        return 1; 
                    }
                }
            }
        }
    }
    return 0; 
}
sub getImage { 
    $person = $_[0]; 
    $image = "<img width=\"200px\" src=\"students/$person/profile.jpg\">";
    return $image; 
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

sub lineHeading { 
    $string = $_[0]; 
    $description = $_[1]; 
    return "<h4><b>$string</b> <i>$description</i></h4>";
}
