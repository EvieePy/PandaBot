CREATE TABLE IF NOT EXISTS rooms(
    gid BIGINT,
    cid BIGINT,
    vid BIGINT,
    PRIMARY KEY (gid, cid)
);


CREATE TABLE IF NOT EXISTS ddragon(
    version TEXT PRIMARY KEY
);