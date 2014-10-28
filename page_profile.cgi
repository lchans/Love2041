#!/usr/bin/perl

sub profilePage { 

	$count = 0; 
    $name = "$_[0]/profile.txt";
	open $profile, "students/$name" or die "Can't open";
	$profile = join ('', <$profile>);
	@text = split ("\n", $profile);

	@images = glob ("$directory/$_[0]/*");
	foreach $image (@images) { 
		if ($image =~ /photo/) { 
			$gallery{$_[0]} .= "<img style='padding: 10px' width=\"100px\" src=\"$image\">";
		}
	}

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
			$line ne $hair && $line ne $degree && line ne $hair && line ne $height && 
			$line ne $weight) { 
			$other .= "$line<br>";
		}
		$count++;
	}

	@sub = split ("<br>", $other);
	foreach $line (@sub) { 
		if ($line =~ /:/) { 
			$header = $line; 
		} else {
			$section{$header} .= "$line<br>"; 
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
				<li class="tab-link current" data-tab="tab-100">Overview</li>
				<li class="tab-link " data-tab="tab-0">Hobbies</li>
				<li class="tab-link" data-tab="tab-1">Movies</li>
				<li class="tab-link" data-tab="tab-2">Bands</li>
				<li class="tab-link" data-tab="tab-3">TV Shows</li>
				<li class="tab-link" data-tab="tab-4">Courses Undertaken</li>
				<li class="tab-link" data-tab="tab-5">Pictures</li>
			</ul>

			<div id="tab-100" class="tab-content current">
				$section{'<b>profile_text:</b>'}
			</div>

			<div id="tab-0" class="tab-content">
				$section{'<b>favourite_hobbies:</b>'}
			</div>
			<div id="tab-1" class="tab-content">
				$section{'<b>favourite_movies:</b>'}
			</div>
			<div id="tab-2" class="tab-content">
				$section{'<b>favourite_bands:</b>'}
			</div>
			<div id="tab-3" class="tab-content">
				$section{'<b>favourite_TV_shows:</b>'}
			</div>
			<div id="tab-4" class="tab-content">
				$section{'<b>courses:</b>'}
			</div>
			<div id="tab-5" class="tab-content">
				$gallery{$_[0]}
			</div>


		</div>
		</div>
	</div>
	</div>
	~; 
}

1;
