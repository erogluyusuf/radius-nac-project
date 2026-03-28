INSERT INTO radcheck (username, attribute, op, value) VALUES ('admin', 'Cleartext-Password', ':=', 'testing123');
INSERT INTO radcheck (username, attribute, op, value) VALUES ('AA:BB:CC:DD:EE:FF', 'Calling-Station-Id', '==', 'AA:BB:CC:DD:EE:FF');

INSERT INTO radusergroup (username, groupname, priority) VALUES ('admin', 'IT_Admin', 1);
INSERT INTO radusergroup (username, groupname, priority) VALUES ('AA:BB:CC:DD:EE:FF', 'Printers', 1);

INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES ('IT_Admin', 'Tunnel-Type', '=', 'VLAN');
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES ('IT_Admin', 'Tunnel-Medium-Type', '=', 'IEEE-802');
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES ('IT_Admin', 'Tunnel-Private-Group-Id', '=', '10');

INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES ('Printers', 'Tunnel-Type', '=', 'VLAN');
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES ('Printers', 'Tunnel-Medium-Type', '=', 'IEEE-802');
INSERT INTO radgroupreply (groupname, attribute, op, value) VALUES ('Printers', 'Tunnel-Private-Group-Id', '=', '20');