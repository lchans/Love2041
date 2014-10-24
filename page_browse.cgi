#!/usr/bin/perl

require "helper_functions.cgi";

@people = glob ("$directory/*");
$next = min($pageNumber + 8, $#people); 
$previous = max(1, $pageNumber - 8); 

sub browsePageHeader { 
    print qq ~
    <nav class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <form class="navbar-form navbar-left" role="search">
                    <div class="form-group">
                        <input type="text" name="search_term"  class="form-control" /> 
                        <input type="submit" name="Search!" class="btn btn-default" />
                    </div>
                </form>
                <ul class="nav navbar-nav">
                    <li><a href='?page=$next'>Next!</a>
                    <li><a href='?page=$previous'>Previous!</a>
                </ul>
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="?browse_page=true">View All Profiles!</a></li>
                </ul>
            </div>
        </div>
    </nav>
    ~
}

sub browsePageContent { 
    print '<div class="row">';
    print '<div class="container">';
    createPreview();
    print '</div></div>';
}


sub createPreview { 
    print $previous;
     for ($i = $previous; $i < $pageNumber; $i++) { 
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
            printProfile();
        }
        $flag = 0; 
        print '</div>';
    }
}

sub printProfile { 
    print getImage($person); 
    print qq~
    <username>$person</username><br>
    <description>$realName, $age</description><br>
    <a href="?profile_page=true&amp;view_person=$person">Go to Profile!</a>
    ~;
}

1;