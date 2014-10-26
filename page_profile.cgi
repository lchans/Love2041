#!/usr/bin/perl

sub profilePage { 

	$count = 0; 
    $name = "$_[0]/profile.txt";
	open $profile, "students/$name" or die "Can't open";
	$profile = join ('', <$profile>);
	@text = split ("\n", $profile);

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
		} elsif ($line =~ /^degree:/) {
			$degree = $text [$count + 1];
		} elsif ($line =~ /^weight:/) { 
			$weight = $text [$count + 1];
		} elsif ($line =~ /^hair/) { 
			$hair = $text [$count + 1];
		} elsif ($line =~ /^height:/) { 
			$height = $text [$count + 1];
		} elsif ($line =~ /:$/) {
			$other .= "<b>$line</b><br>";
		} elsif ($line ne $name && $line ne $username 
			&& $line ne $password && $line ne email && 
			$line ne $email && $line ne $birthdate && $line ne $gender &&
			$line ne $hair && $line ne $degree && line ne $hair && line ne $height) { 
			$other .= "$line<br>";
		}
		$count++;
	}

	@sub = split ("<b>", $other);
	foreach $line (@sub) { 
		if ($line =~ /favourite/) { 
			$interests .= "<b>$line"; 
		} elsif ($line =~ /courses/) { 
			$courses .= "<b>$line";
		}
	}



	print qq ~ 
	<div class="container">
	<div class="row"> 
		<div class="col-md-3">
			<h2>Profile</h2>
			<img width="200px" src="students/$_[0]/profile.jpg"><br>
				<b> Username: </b> $username <br>
				<b> Name:</b>  $name<br>
				<b> Gender:</b>  $gender<br>
				<b> Email: </b> $email<br>
				<b> Birthdate:</b>  $birthdate <br>
				<b> Degree: </b> $degree <br><br>
				<b> Weight: </b> $weight <br>
				<b> Height: </b> $height <br>
				<b> Hair Colour: </b> $hair <br> 
		</div>
		<div class="col-md-9">
			<h2>More Info</h2>
			<ul class="tabs">
			<li class="tab-link current" data-tab="tab-2">Interests</li>
			<li class="tab-link" data-tab="tab-3">Courses Undertaken</li>
			</ul>

			<div id="tab-2" class="tab-content current">
			$interests
			</div>
			<div id="tab-3" class="tab-content">
			$courses
			</div>
		</div>
		</div>
	</div>
	</div>
	~; 
}

1;
