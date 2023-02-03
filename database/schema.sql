CREATE TABLE IF NOT EXISTS rooms(
    gid BIGINT,
    cid BIGINT,
    vid BIGINT,
    PRIMARY KEY (gid, cid)
);