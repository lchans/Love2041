#!/usr/bin/perl

sub homePage { 
    print qq ~
    <div class="container contain">
    <center>
    <h5>&#x2764TWOXFORONE</h5>
        <div class="col-md-4 col-md-offset-4">
        ~;
        if (defined $_[0]) { 
            print qq ~
            $_[0]<br><br>
            ~
        }
        print qq ~ 
        <form method="POST">
            <input type="text" placeholder="Username" name="login" class="form-control"><br>
            <input type="password" placeholder="Password" name="password"  class="form-control"><br>
            <input type="submit" value="Login!"  class="btn btn-default">
        </form><br>
        <a href="?register_page=true">Don't have an account? Register here!</a>
        </div>
    </center>
    </div>
    ~;
}

1;