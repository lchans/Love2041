#!/usr/bin/perl
use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
    use CGI::Cookie;


my $login = param('login');
my $password = param('password');

if (defined $login && defined $password) {
    my $u = CGI::Cookie->new(
    -name => 'username',
    -value => $login,
    );

    my $p = CGI::Cookie->new(
    -name => 'password',
    -value => $password,
    );
    print "Set-Cookie: $u\n";
    print "Set-Cookie: $p\n";
}

      
print "Content-type: text/html\n\n";
print '
<html>
<head> 
<title>LOVE2041</title> 
<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
<link href="http://fonts.googleapis.com/css?family=Oswald:400,700,300" rel="stylesheet" type="text/css">
<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" rel="stylesheet" type="text/css">
<link href="custom.css" rel="stylesheet">
</head>';

$directory = "./students";
$homePage = param('home_page'); 
$browsePage = param('browse_page'); 
$profilePage = param('profile_page');
$searchPage = param('search_page'); 
$searchTerm = param('search_term');
$registerPage = param('register_page');
$person = param('person');
$j = param('page') || 0; 


if (authenticate()) { 
    if (defined $homePage) { 
        print '<center>';
        print '<h5> LOVE2041</h5>'; 
        loginPage();
        print goRegisterPage();
        print '</center>';
    } elsif (defined $browsePage) { 
        browsePageHeader();
        browsePageContent();
    } elsif (defined $profilePage) { 
        profilePage();
        print goBrowsePage();
    } elsif (defined $searchPage) { 
        print param('what');
        searchPageContent();
    } else { 
        browsePageHeader();
        browsePageContent();
    } 
} else { 
    print '<center>';
    print '<h5> LOVE2041</h5>'; 
    loginPage();
    print goRegisterPage();
    print '</center>';
}

print '</html>';

sub browsePageHeader { 
    %cookies = CGI::Cookie->fetch;
    my $login = $cookies{'username'}->value;
    @people = glob ("$directory/*");
    print ' 
    <nav class="navbar navbar-default" role="navigation">
    <div class="container">
    <div class="navbar-header">
    <h6>LOVE2041  </h6>
    </div>
    <form class="navbar-form navbar-left" role="search">';
    print searchbar();
    $k = $j + 8;
    print "Showing profiles $j to $k<br>";
    print "current logged in as: $login";
    print'</form><div><ul class="nav navbar-nav navbar-right">'; 

    print '<li>';
    print goHomePage();
    print '</li>';
    print '<li>';
    if ($k < $#people) {
    print goNextPage();
    }
    print '</li><li>';
    if ($j > 0) {
    print goPreviousPage();
    }
    print '</li><li>';
        print gologout();
        print '</li>';

    print '</ul></div></div></nav>';

}

sub authenticate {
    %cookies = CGI::Cookie->fetch;
    my $password = $cookies{'password'}->value;
    my $login = $cookies{'username'}->value;
    open $file, "username.txt" or die;
    $file = join ('', <$file>);
    @text = split("\n", $file);
    foreach $line (@text) { 
        if ($line eq "$login $password" ) { 
            return 1;
        }
    } 
    return 0; 
}


sub getImage { 
    $person = $_[0]; 
    $image = "<img width=\"200px\"  src=\"students/$person/profile.jpg\">";
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

sub browsePageContent { 
    @people = glob ("$directory/*");
    print '<div class="container">';
    $j = min ($j + 8, $#people);
    for ($i = $j - 8; $i < $j; $i++) { 
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
        }
        print getImage($person); 
        print "<username>$person</username><br>";
        print "<description>$realName, $age</description>";
        print goProfilePage();
        print '</div>';

    }
    print "</div>";
}

sub searchbar { 
    param('search_page', 'true');
    return 
        start_form, 
        hidden('search_page', $searchPage), 
        textfield (
            -name=>'search_term',
            -class=>'form-control',
        ),
        submit (            
            -name=>'Search!',
            -class=>"btn btn-default",
        ), 
        end_form, 
}

sub searchPageContent { 
    print browsePageHeader();
    @people = glob ("$directory/*");
    for ($i = 0; $i < $#people; $i++) { 
        $person = getUsername($people[$i]);
        @text = getProfile ($person);;
        foreach $line (@text) { 
            if ($line =~ /$searchTerm/i) { 
                print '<center><div class="col-md-2">';
                print "<h4>$name</h4>";
                print getImage($person);
                print goProfilePage();
                print '</div></center>';
                break;
            }
        }
    }  
}

sub profilePage { 
print '<div class="row">';
    print '<div class="col-md-6">';
    print getImage($person);
    print '</div>';
    $name = "$person/profile.txt";
	open $profile, "students/$name" or die;
	$profile = join ('', <$profile>);
	@text = split ("\n", $profile);
	print '<div class="col-md-6">';
	foreach $line (@text) { 
		if ($line =~ /:$/) {
			print "<b>$line</b><br>";
		} else { 
			print"$line<br>";
		}
	}
	print '</div>';
	print '</div>';
}


sub loginPage {
    param('browse_page', 'true');
    print start_form,
        hidden ('browse_page', $browsePage), 
        textfield('login'), 
        password_field('password'),
        submit(
            -name=>'Begin!',
            -class=>"btn btn-default",
        ),  
        end_form,
}

sub goProfilePage { 
    param('profile_page', 'true'); 
    return 
        start_form, 
        hidden('profile_page', $profilePage), 
        hidden('person', $person), 
        submit (
            -name=>'View Information!',
            -class=>"btn btn-default",), 
        end_form, 
}

sub goHomePage { 
    param('home_page', 'true');
    return
        start_form,
        hidden ('home_page', $homePage), 
        submit(
            -name=>'Back to home!',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub goRegisterPage { 
    param('register_page', 'true');
    return
        start_form,
        hidden ('register_page', $registerPage), 
        submit(
            -name=>'Register!',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub goBrowsePage { 
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        submit(
            -name=>'Begin!',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub goNextPage { 
    param('page', $j + 8);
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        hidden ('page', $j + 8), 
        submit(
            -name=>'Next',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub goPreviousPage { 
    param('page', $j - 8);
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        hidden ('page', $j - 8), 
        submit(
            -name=>'Previous',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub gologout { 
    logout();
    param('home_page', 'true');
    return
        start_form,
        hidden ('home_page', $homePage), 
        submit(
            -name=>'Logout!',
            -class=>"btn btn-danger",
        ),  
        end_form, 
}


sub logout { 
    my $p = CGI::Cookie->new(
        -value   => '',
        -path    => '/',
        -expires => '-1d'
    );

    my $u = CGI::Cookie->new(
        -value   => '',
        -path    => '/',
        -expires => '-1d'
    );
}

