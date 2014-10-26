#!/usr/bin/perl

@people = glob ("$directory/*");

sub browsePageHeader { 
    $next = $pageNumber + 8; 
    $previous = $pageNumber - 8; 
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
                    <li><p class="navbar-text">Currently logged in as: $login</p></li>
                </ul>
                <ul class="nav navbar-nav navbar-right">
                <li><a href="?my_page=true">My Profile</a></li>
                    <li><a href="?browse_page=true">View All Profiles!</a></li>
                     <li><a href="?logout_page=true">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav>
    ~
}

sub browsePageContent { 
    @people = glob ("$directory/*");
    print '<div class="row">';
    print '<div class="container">';
    createPreview();
    print '</div></div>';
}


sub createPreview { 
    $pageNumber = min ($pageNumber + 8, $#people);
     for ($i = $pageNumber - 8; $i < $pageNumber; $i++) { 
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
    print qq ~
    <username>$person</username><br>
    <description>$realName, $age</description><br>
    <a href="?profile_page=true&view_person=$person">Go to Profile!</a>
    ~
}

1;