#!/usr/bin/perl

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

        if ($line =~ /min:/ && $text[$count] =~ /kg/) { 
            $minWeight = $text[$count];
            $minWeight =~ s/kg//g;
        } elsif ($line =~ /max:/ && $text[$count] =~ /kg/) {
            $maxWeight = $text[$count]; 
            $maxWeight =~ s/kg//g;
        }

        if ($line =~ /max:/ && $text[$count] =~ /m/) { 
            $maxHeight = $text[$count];
        } elsif ($line =~ /max:/) { 
            $maxAge = $text[$count];
        } 

        if ($line =~ /hair_colours:/) { 
            $hair = $text[$count];
        }
    }

    @people = glob ("$directory/*");
    foreach $person (@people) { 
       $user =  getUsername($person);
       $score{$user} = 0;
       @text = getProfile($user);
       $count = 0; 
       foreach $line (@text) {
            $count++; 
            if ($line =~ /gender:/ && $text[$count] =~ /^$gender/) { 
                $score{$user} = $score{$user} + 50;
            } elsif ($line =~ /height:/) { 
                if (($text[$count] > $minHeight) && ($text[$count] < $maxHeight)) { 
                    $score{$user} = $score{$user} + 10;
                }
            } elsif ($line =~ /weight:/) { 
                $weight = $text[$count];
                $weight =~ s/kg//g;
                if (($weight > $minWeight) && ($weight < $maxWeight)) { 
                    $score{$user} = $score{$user} + 10;
                }
            } elsif ($line =~ /birthdate:/) { 
                    $age = convertAge($text[$count]);
                if (($age > $minAge) && ($age < $maxAge)) { 
                    $score{$user} = $score{$user} + 30;
                } elsif (abs($age - $minAge) < 10 || abs($age - $maxAge) < 10) { 
                    $score{$user} = $score{$user} + 20;
                } elsif (abs($age - $minAge) < 20 || abs($age - $maxAge) < 20) { 
                    $score{$user} = $score{$user} + 10;
                }
            } elsif ($line =~ /hair_colour:/) {
                if ($text[$count] =~ /$hair/) { 
                    $score{$user} = $score{$user} + 10;
                }
            } 
       }
    }
    @sorted = sort { $score{$b} cmp $score{$a} } keys %score; 
    @people = @sorted; 
    createMatch();
}

sub createMatch { 
    print '<div class="container">';
    $pageNumber = min ($pageNumber + 8, $#people);
     for ($i = $pageNumber - 8; $i < $pageNumber; $i++) { 
        if (defined getUsername($people[$i])) { 
            $person = getUsername($people[$i]);
            @text = getProfile ($person);
            $count = 0; 
            foreach $l (@text) { 
               $count++; 
               if ($l =~ /^.+:/)  {
                    $l =~ s/://g;
                    $user{$l} = $text[$count];
               }
            }           
            $percent = floor($score{$person} / $score{@people[0]}) || 0;
            $percent = $score{$person};
            printPage();
 
        }
    }
    matchFooter();
    print '</div>';
}


sub printPage { 
    $age = convertAge($user{'birthdate'});
    print qq ~
        <div class="col-md-3">
        <img width="200px" src="students/$person/profile.jpg"><br>
        <username>$person</username><br>
        <description>$user{name}, $age</description><br>
        <a href="?profile_page=true&view_person=$person">Go to Profile!</a><br>
        Compatability Score: \% $percent<br>
        </div>
    ~;
}

sub matchFooter { 
    $next = min($pageNumber, $#people); 
    $previous = $next - 16;
    print qq ~ 
    <center>
    <a href='?page=$previous&match_page=true&matched=true'>
        <span style="font-size:20px; color: #000000" class="glyphicon glyphicon-chevron-left">
        </span>
    </a>
    <a href='?page=$next&match_page=true&matched=true'>
        <span style="font-size:20px; color: #000000" class="glyphicon glyphicon-chevron-right">
        </span>
    </a>
    </center>
    <br><br>
    ~;
}

1;
