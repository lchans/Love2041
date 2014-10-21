#!/usr/bin/perl

require "helper_functions.cgi";

sub browsePageHeader { 
    my $login = getLogin();
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
    print "<p class=\"navbar-text\">Currently logged in as: $login</p>";
    print'</form><div><ul class="nav navbar-nav navbar-right">'; 
    print '<li>';
    print goBrowsePage();
    print '</li>';
    print'<li>';
    print gologout();
    print '</li>';
    print '</ul></div></div></nav>';
}

sub browsePageContent { 
    @people = glob ("$directory/*");
    $j = min ($j + 8, $#people);
    print '<div class="row"><div class="col-md-1">';
    if ($j - 8 > 0) {
    print goPreviousPage();
    }
    print '</div>';
    print '<div class="col-md-10">';
    print '<div class="container">';
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
           if ($l =~ /$searchTerm/i) { 
                $flag = 1; 
           }
        }
        if ($flag == 1 || !(defined $searchTerm)) { 
            print getImage($person); 
            print "<username>$person</username><br>";
            print "<description>$realName, $age</description>";
            print goProfilePage();
        }
        $flag = 0; 
        print '</div>';

    }
    $j = $j - 8;
    print '</div></div>';
    print '<div class="col-md-1">';
    if ($k < $#people) {
    print goNextPage();
    }
    print '</div></div>';
    print "<center>";
    print "Showing profiles $j to $k<br><br>";
    print "</center>";

}

1;