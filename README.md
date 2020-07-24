# orthomcl
Pipeline for the OrthoMCL software

Include all the steps described in the User guide.

Depending on the size of input dataset size (number of FASTA sequences), the MySQL may return the following error:

## DBD::mysql::st execute failed: The total number of locks exceeds the lock table size at orthomclSoftware-v2.0.9/bin/orthomclPairs line 709, <F> line 12.

Fix the error:\
mysql> SET GLOBAL innodb_buffer_pool_size=402653184;\


## ERROR 1698 (28000): Access denied for user 'root'@'localhost'

mysql> sudo mysql -u root
mysql> USE mysql;
mysql> SELECT User, Host, plugin FROM mysql.user;
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
mysql> FLUSH PRIVILEGES;
mysql> exit;
mysql> sudo service mysql restart

mysql> sudo mysql -u root
mysql> USE mysql;
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';
mysql> FLUSH PRIVILEGES;
mysql> exit;


## The default root password is blank (i.e. empty string) 

$ mysqladmin -u root password [newpassword]
