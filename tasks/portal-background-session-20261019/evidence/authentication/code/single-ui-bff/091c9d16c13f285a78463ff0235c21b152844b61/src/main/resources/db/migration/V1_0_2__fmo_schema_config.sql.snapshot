CREATE SEQUENCE IF NOT EXISTS post_trade_portal_service.application_session_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

CREATE TABLE IF NOT EXISTS post_trade_portal_service.application_session
(
    application_session_id bigint NOT NULL,
    created_at timestamp NOT NULL DEFAULT NOW(),
    session_id character varying(32000) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT application_session_pkey PRIMARY KEY (application_session_id)
)
TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS application_session_0_idx
ON post_trade_portal_service.application_session USING btree (created_at)
TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS application_session_1_idx
ON post_trade_portal_service.application_session USING btree (session_id)
TABLESPACE pg_default;

CREATE FUNCTION post_trade_portal_service.application_session_delete_old_rows() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  DELETE FROM application_session WHERE created_at < NOW() - INTERVAL '15 minute';
  RETURN NEW;
END;
$$;

CREATE TRIGGER application_session_delete_old_rows_trigger
    AFTER INSERT ON post_trade_portal_service.application_session
    EXECUTE PROCEDURE post_trade_portal_service.application_session_delete_old_rows();