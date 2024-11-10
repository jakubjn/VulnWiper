<?php

namespace SampleWebsite;

use mysqli;

class Dbconnection
{
    private $servername;
    private $username;
    private $password;
    private $dbname;

    public function __construct($servername, $username, $password, $dbname)
    {
        $this->servername = $servername;
        $this->username = $username;
        $this->password = $password;
        $this->dbname = $dbname;
    }

    public function get_Connection() : mysqli
    {
        $connection = mysqli_connect($this->servername, $this->username, $this->password, $this->dbname);

        if (!$connection) {
            die("Connection failed: " . mysqli_connect_error());
        }

        return $connection;
    }
}

