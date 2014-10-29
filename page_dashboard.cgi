#!/usr/bin/perl

sub dashboard { 
    print qq ~
        <center>
        <div class="col-md-8 col-md-offset-2">
            <div class="col-md-4">
                <span style="font-size: 100px" class="glyphicon glyphicon-user">
                    <h6><a href="?my_page=true">VIEW MY PROFILE</a></h6>
            </div>
            <div class="col-md-4">
                <span style="font-size: 100px"class="glyphicon glyphicon-pencil">
                    <h6><a href="?edit_page=true">CHANGE MY PROFILE</a></h6>
            </div>
            <div class="col-md-4">
                <span style="font-size: 100px" class="glyphicon glyphicon-remove">
                <h6><a href="?delete_profile=true">DELETE MY PROFILE</a></h6>
            </div>
        </div>
        </center>
    ~;
}

sub editProfile { 
    %s = getHash();
    @hashKey = keys %s; 
    print qq~
    <div class="container">
    <div class="col-md-8 col-md-offset-2">
    <form role="form" method="POST">~; 
    foreach $keys (@hashKey) { 
        print qq ~
        <label>$keys</label>
        <textarea class="form-control" value="$keys" name="$keys">
        $s{$keys}
        </textarea><br>
        </input><br>
        ~;
    }
    print qq~
    <input type="submit" value="Change text!" name="change_text" class="btn btn-default btn-sm">
    </form>
    </div>
    </div>
    ~;
}

sub changeProfile { 
    open $profile, ">", "students\/$login\/profile.txt" or die;
    @profile = split("\n", $profile);
    foreach $line (@profile) { 
        if ($line =~ /:/) { 
            $tabs{$line} = "";
        } 
    }
    @keys = keys %tabs; 
    foreach $key (@keys) { 
        print $profile $key, "\n"; 
        print $profile param("$key"), "\n";
    }
}

sub getHash { 
    open $profile, "<", "students\/$login\/profile.txt" or die;
    @sub =  split ("\n", $profile);
    foreach $line (@sub) { 
        if ($line =~ /:/) { 
            $header = $line;
            $tabs{$header} = ""; 
        } else {
            $tabs{$header} .= "$line\n"; 

        }
    }
    return %tabs;
}

1;