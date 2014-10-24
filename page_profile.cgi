#!/usr/bin/perl

# getLogin - returns login from cookie
# getPassword - returns password from cookie
# getImage - returns image from a given username (AwesomeGirl40)
# getProfile - gets profile in plain text from given username (AwesomeGirl40)
# getUsername - gets username from directory (./students/AwesomeGirl40)

require "helper_functions.cgi";

sub profilePage { 
	$count = 0; 
	print '<div class="row"><div class="container">';

    $name = "$person/profile.txt";
	open $profile, "students/$name" or die "Can't open";
	$profile = join ('', <$profile>);
	@text = split ("\n", $profile);
	print '<div class="col-md-6">';
	print '<h1>Interests</h1>';
	foreach $line (@text) { 
		if ($line =~ /^name:/) { 
			$name = $text[$count + 1];
		} elsif ($line =~ /^username:/) { 
			$username = $text[$count + 1];
		} elsif ($line =~ /^password:/) { 
			$password = $text[$count + 1];
		} elsif ($line =~ /^email:/) { 
			$email = $text[$count + 1];
		} elsif ($line =~ /^birthdate:/) { 
			$birthdate = $text[$count + 1];
		} elsif ($line =~ /^gender:/) { 
			$gender = $text[$count + 1];
		} elsif ($line =~ /^hair colour:/) { 
			$hair = $text[$count + 1];
		} elsif ($line =~ /:$/) {
			print "<b>$line</b><br>";
		} elsif ($line ne $name && $line ne $username 
			&& $line ne $password && $line ne email && 
			$line ne $email && $line ne $birthdate && $line ne $gender &&
			$line ne $hair) { 
			print"$line<br>";
		}
		$count++;
	}
	print '</div>';

	print '<div class="col-md-6">';
	print '<h1>Profile</h1>';
    print getImage($person);
    print "<br>";
    print lineHeading ("Username: ", $username);
    print lineHeading ("Name: ", $name);
	print lineHeading ("Gender: ", $gender);
	print lineHeading ("Email: ", $username);
	print lineHeading ("Birthdate: ", $birthdate);
	print lineHeading ("Hair Color: ", $hair);
    print '</div></div>';
	print '</div>';
}

1;
