#!/usr/bin/perl
# before using the script issue the following
# sudo cpan
# then issue....
# install REST::Client
#
use REST::Client;
my $client = REST::Client->new();
$client->getUseragent()->ssl_opts(verify_hostname => 0);
$client->getUseragent()->ssl_opts(SSL_verify_mode => SSL_VERIFY_NONE);
# $client->addHeader(‘X-DreamFactory-API-Key’, ‘YOUR_API_KEY’);
# $client->addHeader(‘cache-control’, ‘no-cache’);
$client->GET("http://api.open-notify.org/astros.json");
print $client->responseContent();
