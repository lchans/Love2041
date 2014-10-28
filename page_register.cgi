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
	if (param('username') eq "") { 
		print "Please enter a username!";
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
	return 1; 
}

sub confirmRegistration { 

	$username = param('username');
	$email = param('email');

	#makeProfile ($username);

	$activate{$username} = crypt ($username, 'lc');

	$message = "$username, this e-mail is here to confirm your registration for TWOXFORONE\n
				Please click the link below to activate your account:\n
				cgi.cse.unsw.edu.au/~lchan/love2041/love2041.cgi?$activate{$username}";

  	send_email('administrator@twoxforone.com',
             $email,
             'Confirm you account for TWOXFORONE',
             $message);

	print qq ~ 
		<center> A confirmation e-mail has been sent to $email.<br>
		Please click on the link to activate your account!

	    <form class="form-horizontal" action='' method="POST">
	    <input type="submit" value="Go back!" name="?logout_page=true" class="btn btn-default">
	    </form>
	    </center>
	~;
}

sub makeProfile { 
	$dir = "students/$_[0]";
	mkdir($dir);
	open my $file, ">>students/$_[0]/preferences.txt";
	print $file "default";
	close $file;
	open my $file,">>students/$_[0]/profile.txt";
	print $file "default";
	close $file;
}

sub send_email {
    my ($sender, $receiver, $subject, $message_content) = @_;
    open(MAIL, "|/usr/lib/sendmail -oi -t");
    print MAIL "From: $sender\n";
    print MAIL "To: $receiver\n";
    print MAIL "Subject: $subject\n\n";
    print MAIL "$message_content\n";
    close(MAIL);
}




1;