#!/usr/bin/perl

=HOME PAGE 
    Prints the HTML of the front page. Parameters are login and password. 
    Other parameters are recover_page, which when clicked, goes to a recover 
    password page and register_page, which goes to the registration form. 
=cut
sub homePage { 
    if (defined $_[0]) { $warning = $_[0] };
    print qq ~
    <div class="container contain">
    <center>
    <h5>&#x2764TWOXFORONE</h5>
        <div class="col-md-4 col-md-offset-4">
        $warning <br> <br>
        <form method="POST">
            <input type="text" placeholder="Username" name="login" class="form-control"><br>
            <input type="password" placeholder="Password" name="password"  class="form-control"><br>
            <input type="submit" value="Login!"  class="btn btn-default">
        </form><br>
        <a style="color: #000000" href="?recover_page=true">Forgot your password?</a><br>
        <a style="color: #000000" href="?register_page=true">Don't have an account? Register here!</a>
        </div>
    </center>
    </div>
    ~;
}

1;