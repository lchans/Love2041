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
    print qq~
    <div class="container">
    <div class="col-md-8 col-md-offset-2">
    <form role="form">
    <textarea class="form-control" name='edited'></textarea>
    <input type="submit" value="Change text!" name="add_text" class="btn btn-default">
    </input>
    </form>
    </div>
    </div>
    ~;
}

sub addText { 
    open $profile, ">>", "students/$login/profile.txt" or die;
    print $profile "\nprofile_text:\n";
    print $profile "\t$edited";
}

1;