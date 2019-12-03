# orthomcl
Pipeline for the OrthoMCL software

Include all the steps described in the User guide.

Depending on the size of input dataset size (number of FASTA sequences), the MySQL may return the following error:

DBD::mysql::st execute failed: The total number of locks exceeds the lock table size at orthomclSoftware-v2.0.9/bin/orthomclPairs line 709, <F> line 12.

Fix the error:
* Enter MySQL: mysql -u root -p
* SET GLOBAL innodb_buffer_pool_size=402653184;
* Quit MySQL.
