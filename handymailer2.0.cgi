#!/usr/bin/perl

##############################
# Jake's Handymailer Script 
# Version 2.0
# June 1998
# for use on jake.net only
# Copyright Jake Peters, 1996
##############################

# Sets the location of the sendmail program on UNIX host computer
$mailprog='/usr/lib/sendmail';

# holds the addresses to be blocked in the to field
@illegalto =   ("misc-activism-militia\@moderators.uu.net",
				"msc-activism-militia\@moderators.uu.net",
				"vicepresident\@whitehouse.gov",
				"president\@whitehouse.gov",
				"oisi\@worldnet.att.net");

# holds the addresses to be blocked in the from field
@illegalfrom = ("jake\@jake.net",
				"jacobp\@wharton.upenn.edu",
				"jacobp\@seas.upenn.edu",
				"jakep\@tiac.net",
				"webmaster\@jake.net",
				"lpeters\@shore.net",
				"jakep93\@hotmail.com".
				"caren\@jake.net",
				"jrpeters\@shore.net");

# reads in the content length ENV var and puts values into associative array
&process_post_cgi_info;

# extracts the info from associative array into string vars for easy access
&set_vars;

# checks to make sure all fields are filled
&errorcheck_empty_field;

# checks to make sure from and to addresses contain an @ and are in the right form
#&verify_address_format;

# checks the to address against the @illegalto block list
&check_to_field;

# checks the from address against the @illegalfrom block list
&check_from_field;

# reports errors if there are any otherwise sends the message
if (@errors > 0) {
	&print_error_page;
} else {
&print_response;  # prints out the confirmation page
&sendmsg;         # mails the message
&mailme;          # mails me a copy w/ IP info
}


###########################################
#            THE SUBROUTINES              #
###########################################

###################################
# Processing the POST information #
###################################
sub process_post_cgi_info {
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
}

##########################
# set the prog variables #
##########################
sub set_vars {
$to="$FORM{'to'}";
$from="$FORM{'from'}";
$subject="$FORM{'subject'}";
$body="$FORM{'body'}";
@errors = (); #used for error handling later
}

##########################
# Check for empty fields #
##########################
sub errorcheck_empty_field {
foreach $item(keys(%FORM)) {
	if ($FORM{$item} eq "") {
		push(@errors,"The $item field is blank and needs to be filled.");
	}
}
}

#########################################
# Check verify format of address fields #
#########################################

#sub verify_address_format {
#if ($from =~ /([\w\-\+]+)@([\w\-\+\.]+)/)) {} else {
#	push(@errors,"The address in the FROM field needs to be in the format of ---@---.--- (example john@smith.com)");
#}
#
#if $to=~/([\w\-\+]+)@([\w\-\+\.]+)/) {} else {
#	push(@errors,"The address in the TO field needs to be in the format of ---@---.--- (example john@smith.com)");
#}
#}



############################################
# Check the To field for blocked addresses #
############################################

sub check_to_field {
foreach $valueto(@illegalto) {
	if ($to eq $valueto) {
	 push(@errors,"The TO field cannot have a value of $to.  It is not allowed.");
	}
}
}

##############################################
# Check the FROM field for blocked addresses #
##############################################

sub check_from_field {
foreach $valuefrom(@illegalfrom) {
	if ($from eq $valuefrom) {
		push(@errors,"The FROM field cannot have a value of $from.  It is not allowed.");
	}
}
}


############################
# Print out the error page #
############################

sub print_error_page {
print "Content-Type:text/html","\n\n"; 
print "<html><head><title>Error!</title></head>\n";
print <<END
<body bgcolor="#000080" text="#FFFFFF" link="#00FF00" vlink="#00FF00">
<font face="arial">
<h2>There were errors in your handymailer form.</h2>
The following errors were found:
END
;

print "<ul>\n";

foreach $desc(@errors) {
	print "<li> $desc \n";
	}
	
print "</ul><P>Please press the back button on your browser and make the changes.</font></body></html>\n";
}

########################################
# Print out the confirmation page code #
########################################
sub print_response {
print <<END
Content-Type:text/html\n\n
<html>
<head><title>Your Mail Was Sent!</title></head>
<body bgcolor="#000060" text="#FFFFFF" link="#00FF00" vlink="#00FF00">
<font face="arial">
<h1><center>Congratulations your mail was sent!</center></h1>
Here is a copy of what was sent:<p>
<hr>
To: $to<br>
From: $from<br>
Subject: $subject<p>
<table border="0" width="90%">
<tr >
<td width="87%" >
$body
</td>
</tr>
</table>

<hr><p>Return to the <a href="../handymailer/index.html">Handymailer page</a></font></body></html>
END
;
}

###########################
# Send the actual message #
###########################
sub sendmsg {
open(MAIL, "|$mailprog $to") || die "can't open $mailprog!\n";
print MAIL "X-Sender: $from\n";
print MAIL "X-mailer: fakemailer\n";
print MAIL "From: $from\n";
print MAIL "To: $to\n";
print MAIL "Subject: $subject\n\n";
print MAIL "$body\n";
print MAIL "\n\n\n\n\n\n\n\n\n\n\n\n";
print MAIL "\n\n\n\n\n\n\n\n\n\n\n\n";
print MAIL "Handymailer Server .. .. ..\n";
print MAIL "www.jake.net/handymailer/\n";
close(MAIL);
}

##########################
# send the message to me #
##########################
sub mailme {
open(MAIL2, "|$mailprog handymailer\@jake.net") || die "can't open
$mailprog!\n";
print MAIL2 "From: $from\n";
print MAIL2 "To: handymailer\@jake.net\n";
print MAIL2 "Subject: $subject\n\n";
print MAIL2 "TO FIELD: $to\n";
print MAIL2 "******************************************************\n";
print MAIL2 "$body\n";
print MAIL2 "\n******************************************************\n";
print MAIL2 "Handymailer Server .. .. ..\n";
print MAIL2 "Remote Addr: $ENV{'REMOTE_ADDR'}\n";
@subnet_numbers = split (/\./, $ENV{'REMOTE_ADDR'});
$packed_address = pack ("C4", @subnet_numbers);
($remote_host) = gethostbyaddr ($packed_address, 2);
print MAIL2 "Remote Host: $remote_host\n";
print MAIL2 "User  Agent: $ENV{'HTTP_USER_AGENT'}\n";
close(MAIL2);
}

###DONE###
exit(0);





