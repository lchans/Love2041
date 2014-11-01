#!/usr/bin/perl

use constant USERNAME_FIELD => 0;
use constant PASSWORD_FIELD => 1;
use constant EMAIL_FIELD => 2;

=ENTERS USERNAME
	- User enters their username into the field to get login details 
=cut
sub enterUsername { 
	print qq~ 
	<form class="form-horizontal" action='' method="POST">
	<label class="control-label" for="username">Please enter your e-mail</label>
	<input type="text" name="email" class="form-control">
	<input type="submit" value="Submit" name="complete_recover" class="btn btn-default">
	</form>
	~; 
}

=AUTHENTICATES USERNAME 
	- Checks the entered username against profile details stored in a textfile. 
	- If a username is found, then an email is sent with a login and password
=cut
sub authenticateUsername { 
	sendPassword();
	$username = param('username');
	print qq ~
	$username- Your login details have been sent to your email. <br>
	Please click on the link to recover your password.<br>
	<form method="POST">
	<input type="submit" value="Go back!" name="home_page" class="btn btn-default">
	</form>
	~;
}

=SEND PASSWORD 
	- Function to create an email to send containing login and password.
=cut
sub sendPassword { 
	$email = param('email');
	open $FILE, "<", "username.txt" or die;
	$FILE = join ('', <$FILE>);
	@data = split ("\n", $FILE); 
	foreach $line (@data) { 
		if ($line =~ /$email/) { 
			@dataset = split(" ", $line);
			$message = "$dataset[USERNAME_FIELD], this e-mail contains your login details for TWOXFORONE\n
			Username: $dataset[USERNAME_FIELD]\n
			Password: $dataset[PASSWORD_FIELD]";
			send_email('administrator@twoxforone.com',$dataset[EMAIL_FIELD],'Login details for TWOXFORONE', $message);
			print $dataset[EMAIL_FIELD];
			break;
		}
	}
}

1;