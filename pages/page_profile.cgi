#!/usr/bin/perl

sub printProfile {
	@text = getProfile($_[0]);
	@images = glob ("$directory/$_[0]/*");
	foreach $image (@images) { 
		if ($image =~ /photo/) { 
			$gallery{$_[0]} .= "<img style='padding: 10px' width=\"100px\" src=\"$image\">";
		}
	}
	%section = getHash($_[0]);
	print qq ~ 
	<div class="container">
	<div class="row"> 
		<div class="col-md-3">
			<h2>Profile</h2>
			<img width="200px" src="students/$_[0]/profile.jpg">
				<b> Username: </b> $section{'username:'}
				<b> Name:</b>  $section{'name:'}
				<b> Gender:</b>  $section{'gender:'}
				<b> Email: </b> $section{'email:'}
				<b> Birthdate:</b>  $section{'birthdate:'}
				<b> Degree: </b> $section{'degree:'}
				<b> Weight: </b> $section{'weight:'}
				<b> Height: </b> $section{'height:'}
				<b> Hair Colour: </b> $section{'hair:'}
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
				$section{'profile_text:'}
			</div>

			<div id="tab-0" class="tab-content">
				$section{'favourite_hobbies:'}
			</div>
			<div id="tab-1" class="tab-content">
				$section{'favourite_movies:'}
			</div>
			<div id="tab-2" class="tab-content">
				$section{'favourite_bands:'}
			</div>
			<div id="tab-3" class="tab-content">
				$section{'favourite_TV_shows:'}
			</div>
			<div id="tab-4" class="tab-content">
				$section{'courses:'}
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
