#!/usr/bin/perl

# getLogin - returns login from cookie
# getPassword - returns password from cookie
# getImage - returns image from a given username (AwesomeGirl40)
# getProfile - gets profile in plain text from given username (AwesomeGirl40)
# getUsername - gets username from directory (./students/AwesomeGirl40)

sub getLogin { 
    %cookies = CGI::Cookie->fetch;
    if (defined $cookies{'username'}->value) { 
        return $cookies{'username'}->value;
    }
    return "Invalid Login!";
}

sub getPassword { 
    %cookies = CGI::Cookie->fetch;
    if (defined $cookies{'password'}->value) { 
        return $cookies{'password'}->value;
    }
    return "Invalid Password!";
}

sub getImage { 
    $person = $_[0]; 
    $image = "<img width=\"200px\" src=\"students/$person/profile.jpg\">";
    return $image; 
}

sub getUsername { 
    $person = $_[0]; 
    $person =~ s/\.\///g;
    $person =~ s/students\///;
    param('person', $person); 
    return $person;
}

sub getProfile { 
    $person = $_[0]; 
    $n = "$person/profile.txt";
    open $profile, "students/$n" or die;
    $profile = join ('', <$profile>);
    @text = split ("\n", $profile);
    return @text; 
}

sub lineHeading { 
    $string = $_[0]; 
    $description = $_[1]; 
    return "<h4><b>$string</b> <i>$description</i></h4>";
}

1;