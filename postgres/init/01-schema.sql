CREATE TABLE radcheck (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL DEFAULT '',
    attribute VARCHAR(64) NOT NULL DEFAULT '',
    op VARCHAR(2) NOT NULL DEFAULT '==',
    value VARCHAR(253) NOT NULL DEFAULT ''
);

CREATE TABLE radreply (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL DEFAULT '',
    attribute VARCHAR(64) NOT NULL DEFAULT '',
    op VARCHAR(2) NOT NULL DEFAULT '=',
    value VARCHAR(253) NOT NULL DEFAULT ''
);

CREATE TABLE radgroupreply (
    id SERIAL PRIMARY KEY,
    groupname VARCHAR(64) NOT NULL DEFAULT '',
    attribute VARCHAR(64) NOT NULL DEFAULT '',
    op VARCHAR(2) NOT NULL DEFAULT '=',
    value VARCHAR(253) NOT NULL DEFAULT ''
);

CREATE TABLE radusergroup (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL DEFAULT '',
    groupname VARCHAR(64) NOT NULL DEFAULT '',
    priority INT NOT NULL DEFAULT 0
);

CREATE TABLE radacct (
    radacctid BIGSERIAL PRIMARY KEY,
    acctsessionid VARCHAR(64) NOT NULL DEFAULT '',
    acctuniqueid VARCHAR(32) NOT NULL DEFAULT '',
    username VARCHAR(64) NOT NULL DEFAULT '',
    realm VARCHAR(64) DEFAULT '',
    nasipaddress INET NOT NULL,
    nasportid VARCHAR(32) DEFAULT NULL,
    nasporttype VARCHAR(32) DEFAULT NULL,
    acctstarttime TIMESTAMP WITH TIME ZONE NULL,
    acctupdatetime TIMESTAMP WITH TIME ZONE NULL,
    acctstoptime TIMESTAMP WITH TIME ZONE NULL,
    acctinterval INT DEFAULT NULL,
    acctsessiontime INT DEFAULT NULL,
    acctauthentic VARCHAR(32) DEFAULT NULL,
    connectinfo_start VARCHAR(128) DEFAULT NULL,
    connectinfo_stop VARCHAR(128) DEFAULT NULL,
    acctinputoctets BIGINT DEFAULT NULL,
    acctoutputoctets BIGINT DEFAULT NULL,
    calledstationid VARCHAR(50) NOT NULL DEFAULT '',
    callingstationid VARCHAR(50) NOT NULL DEFAULT '',
    acctterminatecause VARCHAR(32) NOT NULL DEFAULT '',
    servicetype VARCHAR(32) DEFAULT NULL,
    framedprotocol VARCHAR(32) DEFAULT NULL,
    framedipaddress INET DEFAULT NULL
);

CREATE INDEX radcheck_username ON radcheck(username, attribute);
CREATE INDEX radreply_username ON radreply(username, attribute);
CREATE INDEX radgroupreply_groupname ON radgroupreply(groupname, attribute);
CREATE INDEX radusergroup_username ON radusergroup(username);
CREATE INDEX radacct_active_session ON radacct(acctsessionid, username, nasipaddress);
CREATE INDEX radacct_start_time ON radacct(acctstarttime);