#!/usr/bin/perl

sub registerPage { 
    $warning = "";
    print qq ~ 
    <div class="row">
    <div class="col-md-4 col-md-offset-4">
    <form class="form-horizontal" action='' method="POST">

        <label class="control-label" for="username">Desired username</label>
        <input type="text" id="username" name="username" class="form-control">
        <p class="help-block">Username can contain any letters or numbers, without spaces</p>

        <label class="control-label" for="password">Enter your password</label>
        <input type="password" id="password" name="password" class="form-control">
        <p class="help-block">Password must be at least 6 characters in length</p>

        <label class="control-label" for="passwordCheck">Enter your password again</label>
        <input type="password" id="password" name="passwordCheck" class="form-control">

        <label class="control-label" for="email">Enter your e-mail</label>
        <input type="text" id="email" name="email" class="form-control"><br>

        <input type="submit" value="Register Now!" name="complete_registration" class="btn btn-default">
    </form><br>
    </div>
    </div>
    ~;
    return 1;
}

sub authRegistration { 
	print '<div class="row">';
	if (param('username') eq "") { 
		print "Please enter a username!</div>";
		registerPage();
		return 0;
	} elsif (param('password') ne param('passwordCheck')) { 
		print "Passwords are not the same, enter again!";
		registerPage();
		return 0;
	} elsif (length(param('password')) < 6) { 
		print "Password must be 6 letters or greater!";
		registerPage();
		return 0;
	} elsif (param('email') != /@/) { 
		print "Enter a valid email address!";
		registerPage();
		return 0;
	} 
	print '</div>';
	return 1; 
}

sub confirmRegistration { 
print qq ~ 
    <form class="form-horizontal" action='' method="POST">
    <input type="submit" value="Go back!" name="?logout_page=true" class="btn btn-default">
    </form>
~;
}

1;