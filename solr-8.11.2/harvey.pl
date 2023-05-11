#!/usr/bin/perl
#
# simple OAI-PMH harvester
# hussein suleman
# sometime in 2004 (i think)

$| = 1;

my $baseURL = 'http://union.ndltd.org/OAI-PMH/';

my $filename = 'aaaaaaaa';
my $resumptionToken = '';

use LWP::UserAgent;
$ua = LWP::UserAgent->new;
# before running this script, execute:
#   export http_proxy=http://localhost:<port>/   where <port> is your cntlm port
$ua->env_proxy();

do {
   my $reqURL = $baseURL.'?verb=ListRecords&'.(($resumptionToken eq '')?'metadataPrefix=oai_dc':'resumptionToken='.$resumptionToken);
# my $reqURL = $baseURL.'?verb=Identify';
   my $req = HTTP::Request->new( GET => $reqURL );
   
   print "Harvesting $reqURL\n";
   my $state = 0;
   my $res;
   while ($state == 0)
   {
      $res = $ua->request($req);
      if ($res->code == 503)
      {
         my $sleep = $res->header ('Retry-After');
         if (not defined ($sleep) || ($sleep < 0) || ($sleep > 86400))
         { $state = 1;}
         else
         { 
            print "Sleeping for $sleep seconds\n";
            sleep ($sleep); 
         }
      }
      else
      { $state = 1; }
   }

   my $content = $res->content;
   my $records = (split (/<metadata>/, $content))-1;
   print "Saving response with $records records to $filename.xml\n";
   open (FILE, ">$filename.xml"); print FILE $content; close (FILE);
   $filename++;   
   
   $resumptionToken = '';
   if ($content =~ /<resumptionToken[^>]*>([^<]+)<\/resumptionToken>/)
   {
      $resumptionToken = $1;
   }
} while ($resumptionToken ne '');