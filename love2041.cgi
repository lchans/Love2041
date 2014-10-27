#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Cookie;
use DateTime;


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
$matchPage = param('match_page');
$registerPage = param('register_page');
$completeReg = param('complete_registration');
$pageNumber = param('page') || 0; 

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
    } elsif (defined $profilePage) { 
        browsePageHeader();
        profilePage($viewPerson);
    } elsif (defined $myProfile) { 
        browsePageHeader();
        profilePage($login);
    } elsif (defined $matchPage) { 
        browsePageHeader();
        if (defined $matched) { 
            createMatch();
        } else { 
            matchPage();
        }
    } else { 
        browsePageHeader();
        browsePageContent();
    } 
} elsif (defined $registerPage) { 
    registerPage();
} elsif (defined $completeReg) { 
    completeReg();
} elsif (!authenticate()) { 
    logoutPage("Incorrect Username or Password!");
} else {
    logoutPage();
}

print '</html>';


sub matchPage { 
    @text = getPreferences ($login);
    $count = 0; 
    #gets the preferences of each line:
    foreach $line (@text) { 
        $count++; 
        if ($line =~ /gender:/) { 
            $gender = $text[$count];
        } 
        if ($line =~ /min:/ && $text[$count] =~ /m/) { 
            $minHeight = $text[$count];
        } elsif ($line =~ /min:/) { 
            $minAge = $text[$count];
        }

        if ($line =~ /max:/ && $text[$count] =~ /m/) { 
            $maxHeight = $text[$count];
        } elsif ($line =~ /max:/) { 
            $maxAge = $text[$count];
        }
    }

    print qq~
    Your preferences are: <br>
    Gender: $gender <br>
    Height Range: $minHeight $maxHeight <br>
    Age Range: $minAge $maxAge <br>
    ~;

    @people = glob ("$directory/*");
    foreach $person (@people) { 
       $user =  getUsername($person);
       $score{$user} = 0;
       @text = getProfile($user);
       $count = 0; 
       foreach $line (@text) {
            $count++; 
            if ($line =~ /gender:/ && $text[$count] =~ /^$gender/) { 
                $score{$user} = $score{$user} + 3;
            } elsif ($line =~ /height:/) { 
                if (($text[$count] > $minHeight) && ($text[$count] < $maxHeight)) { 
                    $score{$user}++;
                }
            } elsif ($line =~ /birthdate:/) { 
                $age = $text[$count];
                $age = convertAge($age);
                if (($age gt $minAge) && ($age lt $maxAge)) { 
                    print $user;
                    $score{$user}++;
                }
            }
       }
    }
    @sorted = sort { $score{$b} cmp $score{$a} } keys %score; 
    @people = @sorted; 
    createMatch();
}


sub createMatch { 
    $pageNumber = min ($pageNumber + 8, $#people);
     for ($i = $pageNumber - 8; $i < $pageNumber; $i++) { 
        if (defined getUsername($people[$i])) { 
            print '<div class="col-md-3">';
            $person = getUsername($people[$i]);
            @text = getProfile ($person);
            $count = 0; 
            foreach $l (@text) { 
               $count++; 
               if ($l =~ /^name:/) { 
                    $realName = $text[$count];
               }
               if ($l =~ /^birthdate:/) { 
                    $age = $text[$count];
               } 
               if ($l =~ /^height:/) { 
                    $height = $text[$count];
               }
               if ($l =~ /^birthdate:/) { 
                    $age = $text[$count];
                    $age = convertAge($age);
               }
            }
            printProfile();
            print $gender;

            print "$minHeight $height $maxHeight<br>";
            print "$minAge $age  $maxAge<br>";
            print '</div>';
        }
    }
    print qq ~ 
    <center> <a href='?page=$previous&match_page=true&matched=true'>Previous!</a>
    ------
    <a href='?page=$next&match_page=true&matched=true'>Next!</a> </center>
    ~;
}

sub convertAge { 
    $birth = $_[0];
    @birthArray = split ("\/", $birth);
    $date = DateTime->today; 
    $current = $date->date;
    @currentArray = split ("\-", $current);
    $age = $currentArray[0] - $birthArray[0];
    return $age;
}



sub logoutPage { 
    print qq ~
    <div class="container contain">
    <center>
    <h5>&#x2764TWOXFORONE</h5>
        <div class="col-md-4 col-md-offset-4">
        ~;
        if (defined $_[0]) { 
            print qq ~
            $_[0]<br><br>
            ~
        }
        print qq ~ 
        <form method="POST">
            <input type="text" placeholder="Username" name="login" class="form-control"><br>
            <input type="password" placeholder="Password" name="password"  class="form-control"><br>
            <input type="submit" value="Login!"  class="btn btn-default">
        </form><br>
        <a href="?register_page=true">Don't have an account? Register here!</a>
        </div>
    </center>
    </div>
    ~;
}

sub registerPage { 
    $warning = "";
    print qq ~ 
    <div class="col-md-4 col-md-offset-4">
    <form class="form-horizontal" action='' method="POST">

        <label class="control-label" for="username">Username</label>
        <input type="text" id="username" name="username" class="form-control">

        <label class="control-label" for="password">Password</label>
        <input type="password" id="password" name="password" class="form-control">

        <label class="control-label" for="email">Email</label>
        <input type="text" id="email" name="email" class="form-control"><br>

        <input type="submit" value="Register Now!" name="complete_registration"  class="btn btn-default">
    </form><br>
    </div>
    ~;
    return 1;
}

sub completeReg { 
print qq ~ 
    <form class="form-horizontal" action='' method="POST">
    <input type="submit" value="Go back!" name="?logout_page=true" class="btn btn-default">
    </form>
~;
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
    %cookies = CGI::Cookie->fetch;
    if (exists $cookies{'username'}) {
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
