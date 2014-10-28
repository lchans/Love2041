#!/usr/bin/perl

@people = glob ("$directory/*");


sub browsePageHeader { 
    print qq ~
    <nav style="margin-bottom: 20px; padding: 10px" class="navbar-inverse" role="navigation">
        <div class="container-fluid">
         <div class="navbar-header">
         <h6>&#x2764TWOXFORONE</h6>
         </div>
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <form class="navbar-form navbar-left" role="search">
                    <div class="form-group">
                        <input type="text" name="search_term"  class="input-sm form-control" /> 
                        <input type="submit" name="Search!" class=" btn-sm btn btn-default" />
                    </div>
                </form>
                <ul class="nav navbar-nav">
                    <li><a href='?match_page=true'>MATCH ME &#x2764</a></li>
                </ul>
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="?my_dashboard=true">My Dashboard</a></li>
                    <li><a href="?browse_page=true">View All Profiles!</a></li>
                    <li><a href="?logout_page=true">Logout</a></li>
                </ul>
            </div>
        </div>
    </nav>
    ~
}

sub browsePageContent { 
    $next = min($pageNumber + 8, $#people); 
    $previous = max($pageNumber - 8, 0); 
    @people = glob ("$directory/*");
    print '<div class="row">';
    print '<div class="container">';
    if (defined $searchTerm) {
        createSearchPreview();
    } else { 
        createPreview();
    }
    print '</div>';
    print '</div>';
    if (defined $searchTerm) { 
        navigateSearchFooter();
    } else { 
        navigateFooter(); 
    }

}

sub createSearchPreview { 
    @people = glob ("$directory/*");
    @matched = ();
    foreach $person (@people) { 
        if (defined getUsername($person)) { 
            $person = getUsername($person);
            @text = getProfile ($person);
            foreach $line (@text) { 
                if ($line =~ /$searchTerm/i) { 
                    push (@matched, $person);
                }
            }
        }
    }


    $pageNumber = min ($pageNumber + 8, $#people);
    for ($i = $pageNumber - 8; $i < $pageNumber; $i++) { 
        if (defined getUsername($matched[$i])) { 
            $person = getUsername($matched[$i]);
            @text = getProfile ($person);
            $count = 0; 
            $flag = 0; 
            foreach $l (@text) { 
               $count++; 
               if ($l =~ /^name:/) { 
                    $realName = $text[$count];
               }
               if ($l =~ /^birthdate:/) { 
                    $age = $text[$count];
               }
            }
            previewSection();
        } 
    }

}


sub createPreview { 
    @people = glob ("$directory/*");
    $pageNumber = min ($pageNumber + 8, $#people);
     for ($i = $pageNumber - 8; $i < $pageNumber; $i++) { 
        print $i;
        if (defined getUsername($people[$i])) { 
            $person = getUsername($people[$i]);
            @text = getProfile ($person);
            $count = 0; 
            $flag = 0; 
            foreach $l (@text) { 
               $count++; 
               if ($l =~ /^name:/) { 
                    $realName = $text[$count];
               }
               if ($l =~ /^birthdate:/) { 
                    $age = $text[$count];
               }
            }
            previewSection();
        } 
    }
}



sub previewSection { 
    print qq ~
    <div class="col-md-3">
    <img width="200px" src="students/$person/profile.jpg"><br>
    <username>$person</username><br>
    <description>$realName, $age</description><br>
    <a href="?profile_page=true&view_person=$person">Go to Profile!</a><br>
    </div>
    ~
}

sub navigateFooter { 
    print qq ~ 
    <div class="row">
    <center>
    <a href='?page=$previous'>
    <span style="font-size:20px; color: #000000" class="glyphicon glyphicon-chevron-left">
    </span>
    </a>
    <a href='?page=$next'>
    <span style="font-size:20px; color: #000000" class="glyphicon glyphicon-chevron-right">
    </span>
    </a>
    </center>
    </div>
    ~;
}

sub navigateSearchFooter { 
    print qq ~ 
    <div class="row">
    <center>
    <a href='?page=$previous&search_term=$searchTerm'>
    <span style="font-size:20px; color: #000000" class="glyphicon glyphicon-chevron-left">
    </span>
    </a>
    <a href='?page=$next&search_term=$searchTerm'>
    <span style="font-size:20px; color: #000000" class="glyphicon glyphicon-chevron-right">
    </span>
    </a>
    </center>
    </div>
    ~;
}



1;