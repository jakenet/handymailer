#!/usr/bin/perl

#############################
# Jake's Private Mailer
# Version 1.0
# 07 Nov 1997
# for use on jake.net only
#############################

##
#Processing the POST information
##

print "Content-Type:text/html","\n\n"; #the header info

read(STDIN,$buffer, $ENV{'CONTENT_LENGTH'});

@pairs=split(/&/,$buffer);

foreach $pair(@pairs)
{
($name,$value)=split(/=/,$pair);
$value=~tr/+/ /;
$value=~s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
$value=~s/~!/ ~!/g;
$FORM{$name}=$value;
}

##
#Send the E-mail code
##
##set the mail variables

$mailprog='/usr/lib/sendmail';
$to="$FORM{'to'}";
$from="$FORM{'from'}";
$subject="$FORM{'subject'}";
$body="$FORM{'body'}";
$cc="$FORM{'cc'}";

##send the message

open(MAIL, "|$mailprog $to,handymailer\@jake.net") || die "can't open
$mailprog!\n";
print MAIL "From: $from\n";
print MAIL "Organization: .. .. ..\n";
print MAIL "To: $to\n";
print MAIL "Subject: $subject\n\n";
print MAIL "$body\n";
close(MAIL);


##
#Print out the response page code
##

print <<END

<head><title>Your Mail Was Sent!</title></head>
<body> <h1><center>Congratulations your mail was sent!</center></h1>
Here is a copy of what was sent:<p>
<hr>
To: $to<br>
From: $from<br>
Subject: $subject<p>

<pre>$body</pre>
<hr>
</body>

END
;


###DONE###

exit(0);





