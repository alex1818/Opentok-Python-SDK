import unittest
from six import text_type, u, b, PY2, PY3
from six.moves.urllib.parse import parse_qs
from nose.tools import raises
from sure import expect
import httpretty
from .validate_jwt import validate_jwt_header

from opentok import OpenTok, Session, MediaModes, ArchiveModes, OpenTokException, __version__

class OpenTokSessionCreationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = u('123456')
        self.api_secret = u('1234567890abcdef1234567890abcdef1234567890')
        self.opentok = OpenTok(self.api_key, self.api_secret)

    @httpretty.activate
    def test_create_default_session(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session()

        validate_jwt_header(self, httpretty.last_request().headers[u('x-tb-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        body = parse_qs(httpretty.last_request().body)
        expect(body).to.have.key(b('p2p.preference')).being.equal([b('enabled')])
        expect(body).to.have.key(b('archiveMode')).being.equal([b('manual')])
        expect(session).to.be.a(Session)
        expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.relayed)
        expect(session).to.have.property(u('location')).being.equal(None)

    @httpretty.activate
    def test_create_routed_session(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(media_mode=MediaModes.routed)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-tb-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        body = parse_qs(httpretty.last_request().body)
        expect(body).to.have.key(b('p2p.preference')).being.equal([b('disabled')])
        expect(body).to.have.key(b('archiveMode')).being.equal([b('manual')])
        expect(session).to.be.a(Session)
        expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.routed)
        expect(session).to.have.property(u('location')).being.equal(None)

    @httpretty.activate
    def test_create_session_with_location_hint(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(location='12.34.56.78')

        validate_jwt_header(self, httpretty.last_request().headers[u('x-tb-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        # ordering of keys is non-deterministic, must parse the body to see if it is correct
        body = parse_qs(httpretty.last_request().body)
        expect(body).to.have.key(b('location')).being.equal([b('12.34.56.78')])
        expect(body).to.have.key(b('p2p.preference')).being.equal([b('enabled')])
        expect(session).to.be.a(Session)
        expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.relayed)
        expect(session).to.have.property(u('location')).being.equal(u('12.34.56.78'))

    @httpretty.activate
    def test_create_routed_session_with_location_hint(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(location='12.34.56.78', media_mode=MediaModes.routed)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-tb-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        # ordering of keys is non-deterministic, must parse the body to see if it is correct
        body = parse_qs(httpretty.last_request().body)
        expect(body).to.have.key(b('location')).being.equal([b('12.34.56.78')])
        expect(body).to.have.key(b('p2p.preference')).being.equal([b('disabled')])
        expect(session).to.be.a(Session)
        expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.routed)
        expect(session).to.have.property(u('location')).being.equal(u('12.34.56.78'))

    @httpretty.activate
    def test_create_manual_archive_mode_session(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(media_mode=MediaModes.routed, archive_mode=ArchiveModes.manual)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-tb-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        body = parse_qs(httpretty.last_request().body)
        expect(body).to.have.key(b('p2p.preference')).being.equal([b('disabled')])
        expect(body).to.have.key(b('archiveMode')).being.equal([b('manual')])
        expect(session).to.be.a(Session)
        expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.routed)
        expect(session).to.have.property(u('archive_mode')).being.equal(ArchiveModes.manual)

    @httpretty.activate
    def test_create_always_archive_mode_session(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))

        session = self.opentok.create_session(media_mode=MediaModes.routed, archive_mode=ArchiveModes.always)

        validate_jwt_header(self, httpretty.last_request().headers[u('x-tb-opentok-auth')])
        expect(httpretty.last_request().headers[u('user-agent')]).to.contain(u('OpenTok-Python-SDK/')+__version__)
        body = parse_qs(httpretty.last_request().body)
        expect(body).to.have.key(b('p2p.preference')).being.equal([b('disabled')])
        expect(body).to.have.key(b('archiveMode')).being.equal([b('always')])
        expect(session).to.be.a(Session)
        expect(session).to.have.property(u('session_id')).being.equal(u('1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg'))
        expect(session).to.have.property(u('media_mode')).being.equal(MediaModes.routed)
        expect(session).to.have.property(u('archive_mode')).being.equal(ArchiveModes.always)

    @httpretty.activate
    def test_complains_about_always_archive_mode_and_relayed_session(self):
        httpretty.register_uri(httpretty.POST, u('https://api.opentok.com/session/create'),
                               body=u('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sessions><Session><session_id>1_MX4xMjM0NTZ-fk1vbiBNYXIgMTcgMDA6NDE6MzEgUERUIDIwMTR-MC42ODM3ODk1MzQ0OTQyODA4fg</session_id><partner_id>123456</partner_id><create_dt>Mon Mar 17 00:41:31 PDT 2014</create_dt></Session></sessions>'),
                               status=200,
                               content_type=u('text/xml'))
        self.assertRaises(OpenTokException, self.opentok.create_session, media_mode=MediaModes.relayed, archive_mode=ArchiveModes.always)

    # TODO: all the cases that throw exceptions
    # TODO: custom api_url requests
