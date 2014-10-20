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
 <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css" rel="stylesheet">
 <link href="http://fonts.googleapis.com/css?family=Oswald:400,700,300" rel="stylesheet" type="text/css">
<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,700" rel="stylesheet" type="text/css">
 <link href="custom.css" rel="stylesheet">
 </head>
';
$directory = "./students";
$homePage = param('home_page'); 
$browsePage = param('browse_page'); 
$profilePage = param('profile_page');
$searchPage = param('search_page'); 
$searchTerm = param('search_term');
$registerPage = param('register_page');
$person = param('person');
$j = param('page') || 0; 

    my $login = param('login');
    my $password = param('password');

    if (defined $homePage) { 
        print '<center>';
        print '<h5> LOVE2041</h5>';
        print goBrowsePage();
        print '</center>';
    } elsif (defined $browsePage) { 
        print '<div id="wrapper">';
        sideBar();
        print '<div id="page-content-wrapper">';
        browsePageContent();
        print '</div></div>'
    } elsif (defined $profilePage) { 
        print 'Profile Page';
        print param('person'); 
        print profilePage();
        print goBrowsePage();
    } elsif (defined $searchPage) { 
        print param('what');
        searchPageContent();
    } elsif (defined $registerPage) {
    
    
    
    } else { 
        print '<center>';
        print '<h5> LOVE2041</h5>';
        print loginPage();
        print goRegisterPage();
        print '</center>';
    }

print '</html>';

sub sideBar { 
        @people = glob ("$directory/*");
    print '
        <div id="sidebar-wrapper">
            <ul class="sidebar-nav">
                <h6>LOVE2041  </h6>
                <form class="form-inline" role="search">';
                    print searchbar();
                print'</form>';
        $k = $j + 6;
        print "Showing profiles $j to $k";
        print goHomePage();
        if ($k < $#people) {
        print goNextPage();
        }
        if ($j > 0) { 
        print goPreviousPage();
        }
        print '</ul></div>';
}

sub authenticateUser {
    my $login = param('login');
    my $password = param('password');
    return $login && $password && $login eq "love" && $password eq "love";
}


sub getImage { 
    $person = $_[0]; 
    $image = "<img width=\"200px\"  src=\"students/$person/profile.jpg\">";
    return $image; 
}

sub getUsername { 
    $person = $_[0]; 
    $person =~ s/\.\///g;sub goNextPage { 
    param('page', $j + 6);
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        hidden ('page', $j + 6), 
        submit(
            -name=>'Next',
            -class=>"btn btn-default",
        ),  
        end_form, 
}
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
    $j = min ($j + 6, $#people);
    for ($i = $j - 6; $i < $j; $i++) { 
        print '<div class="col-md-4">';
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
        print "<br><username>$person</username><br>";
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
            -class=>'form-control input-sm',
        ),
        submit (            
            -name=>'Search!',
            -class=>"btn btn-default btn-sm",
        ), 
        end_form, 
}

sub searchPageContent { 

    @people = glob ("$directory/*");
    for ($i = 0; $i < $#people; $i++) { 
        $person = getUsername($people[$i]);
        @text = getProfile ($person);;
        foreach $line (@text) { 
            if ($line =~ /$searchTerm/i) { 
                print '<center><div  The full example is this: class="col-md-2">';
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
    $name = "$person/profile.txt";
    open $profile, "students/$name" or die;
    $profile = join ('', <$profile>);
    param('page', $j - 6);
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        hidden ('page', $j - 6), 
        submit(
            -name=>'Previous',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub getProfile {
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


sub loginPage {
    param('browse_page', 'true');
    print start_form,
         hidden ('browse_page', $browsePage), 
        'Enter login: ', textfield('login'), "<br>\n",
        ' Enter password: ', password_field('password'),, "<br>\n",
               submit(
            -name=>'Begin!',
            -class=>"btn btn-default",
        ),  
        end_form,
        end_html;
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
    param('page', $j + 6);
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        hidden ('page', $j + 6), 
        submit(
            -name=>'Next',
            -class=>"btn btn-default",
        ),  
        end_form, 
}

sub goPreviousPage { 
    param('page', $j - 6);
    param('browse_page', 'true');
    return
        start_form,
        hidden ('browse_page', $browsePage), 
        hidden ('page', $j - 6), 
        submit(
            -name=>'Next',
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
            -name=>'Register',
            -class=>"btn btn-default",
        ),  
        end_form, 
}



