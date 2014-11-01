#!/usr/bin/perl

use constant SINGLE_LINE => 1;

=DASHBOARD
    - HTML for the dashboard page 
    - Includes Bootstrap glyphicons
    - Links to: 
        - View Profile (Implemented)
        - Edit Profile (Implemented, but buggy)
        - Delete Profile (Not implemented)
=cut

sub editProfile { 
    %s = getHash($login);
    @hashKey = keys %s; 
    print qq~
    <div class="container">
    <div class="col-md-8 col-md-offset-2">
    <form role="form" method="POST">~;
    foreach $keys (@hashKey) { 
            if ($keys =~ /^$/) { 
            print $keys;

            } else { 
                $title = $keys; 
                $title =~ s/_/ /g; 
                $title =~ s/^([a-z])/\u$1/;
                $title =~ s/\s([a-z])/ \u$1/;
                if ($keys =~ /favourite/ || $keys =~ /courses/ || $keys =~ /profile_text/) { 
                print qq ~
                <label>$title</label>
                <textarea style="height: 200px" class="form-control" value="$keys" name="$keys">
                $s{$keys}
                </textarea>
                ~;
                } else {
                print qq ~
                <label>$title</label>
                <input type="text" class="form-control" value="$s{$keys}" name="$keys">
                </input>
                ~;
                }
            }
    }
    print qq~
    <input type="submit" value="Change text!" name="change_text" class="btn btn-default btn-sm">
    </form>
    </div>
    </div>
    ~;
}

=CHANGEPROFILE 
    - Gets the parameters entered by the user in the form and then changes the text 
    in the txt document accordingly 
=cut
sub changeProfile { 
    %tabs = getHash($login);
    open $profile, ">", "students\/$login\/profile.txt" or die;
    @keys = keys %tabs; 
    foreach $key (@keys) { 
        print $profile $key, "\n"; 
        print $profile param("$key"), "\n";
    }
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

1;