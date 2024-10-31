<?php
require 'vendor/autoload.php';

define('APPLICATION_NAME', 'Drive API Quickstart');
define('CREDENTIALS_PATH', '~/.credentials/drive-api-quickstart.json');
define('CLIENT_SECRET_PATH', 'client_secret.json');
define('SCOPES', implode(' ', array(
  Google_Service_Drive::DRIVE)
));

/**
 * Returns an authorized API client.
 * @return Google_Client the authorized client object
 */
function getClient() {
  $client = new Google_Client();
  $client->setApplicationName(APPLICATION_NAME);
  $client->setScopes(SCOPES);
  $client->setAuthConfigFile(CLIENT_SECRET_PATH);
  $client->setAccessType('offline');

  // Load previously authorized credentials from a file.
  $credentialsPath = expandHomeDirectory(CREDENTIALS_PATH);
  if (file_exists($credentialsPath)) {
    $accessToken = file_get_contents($credentialsPath);
  } else {
    // Request authorization from the user.
    $authUrl = $client->createAuthUrl();
    printf("Open the following link in your browser:\n%s\n", $authUrl);
    print 'Enter verification code: ';
    $authCode = trim(fgets(STDIN));

    // Exchange authorization code for an access token.
    $accessToken = $client->authenticate($authCode);

    // Store the credentials to disk.
    if(!file_exists(dirname($credentialsPath))) {
      mkdir(dirname($credentialsPath), 0700, true);
    }
    file_put_contents($credentialsPath, $accessToken);
    printf("Credentials saved to %s\n", $credentialsPath);
  }
  $client->setAccessToken($accessToken);

  // Refresh the token if it's expired.
  if ($client->isAccessTokenExpired()) {
    $client->refreshToken($client->getRefreshToken());
    file_put_contents($credentialsPath, $client->getAccessToken());
  }
  return $client;
}

/**
 * Expands the home directory alias '~' to the full path.
 * @param string $path the path to expand.
 * @return string the expanded path.
 */
function expandHomeDirectory($path) {
  $homeDirectory = getenv('HOME');
  if (empty($homeDirectory)) {
    $homeDirectory = getenv("HOMEDRIVE") . getenv("HOMEPATH");
  }
  return str_replace('~', realpath($homeDirectory), $path);
}

// Get the API client and construct the service object.
$client = getClient();
$service = new Google_Service_Drive($client);

// Print the names and IDs for up to 10 files.
$optParams = array(
  'maxResults' => 1,
);
$results = $service->files->listFiles($optParams);

function searchDownFile($title){
     $client = getClient();
     $service = new Google_Service_Drive($client);
     $optParams = array(
     'maxResults' => 100,
     ); 
     $results = $service->files->listFiles($optParams);
     if (count($results->getItems()) == 0) {return null;}
     else{
      

     foreach ($results->getItems() as $file) {
      if ($title == $file->getTitle()){


      $fileId = $file->getid();
      $downloadUrl = $file->getdownloadUrl();
      $meta = downloadFile($service, $fileId, $downloadUrl);
      file_put_contents($title, $meta); }
}}}

function downloadFile($service, $file,$downloadUrl) {

  if ($downloadUrl) {
    $request = new Google_Http_Request($downloadUrl, 'GET', null, null);
    $httpRequest = $service->getClient()->getAuth()->authenticatedRequest($request);echo "\n";echo "\n";
    if ($httpRequest->getResponseHttpCode() == 200) {
       print 'Done :) Please check your file!';echo "\n";  
#      print $httpRequest->getResponseBody();
      return $httpRequest->getResponseBody(); 
    } else {
      // An error occurred.
      return null;print 'this1';
    }
  } else {
    // The file doesn't have any content stored on Drive.
    return null;print 'this2';
  }
}



if (count($results->getItems()) == 0) {
  print "No files found.\n";
} else {
  print "Please relax while DOWNLOADING ...\n";
  foreach ($results->getItems() as $file) {

########################### Insert file name in the function ##############################
    $search = searchDownFile('document.pdf.zip');
    echo $search;
  }
}






