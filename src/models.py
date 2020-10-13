from src import app, db

albums_artists = db.Table('albums_artists', 
    db.Column('album_spotify_id', db.String(128), db.ForeignKey('albums.spotify_id'), primary_key=True),
    db.Column('artist_spotify_id', db.String(128), db.ForeignKey('artists.spotify_id'), primary_key=True),
)

class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, db.Sequence("seq_album_id"))
    spotify_id = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    uri = db.Column(db.String(128), nullable=False)
    href = db.Column(db.String(128), nullable=False)
    album_type = db.Column(db.String(128), nullable=False)
    images = db.Column(db.ARRAY(db.JSON))
    external_urls = db.Column(db.ARRAY(db.JSON))
    available_markets = db.Column(db.ARRAY(db.String(2)))
    artists = db.relationship('Artist',
        secondary=albums_artists,
        lazy='subquery',
        backref=db.backref('albums', lazy='subquery'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def serialize(self, get_artists=True):
        album_dict = {
            "id": self.id,
            "spotify_id": self.spotify_id,
            "name": self.name,
            "uri": self.uri,
            "href": self.href,
            "album_type": self.album_type,
            "images": self.images,
            "external_urls": self.external_urls,
            "available_markets": self.available_markets,
            "created_at": self.created_at.isoformat(),
        }
        if get_artists:
            album_dict["artists"] = [artist.serialize(get_albums=False) for artist in self.artists]
        return album_dict

class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, db.Sequence("seq_artist_id"))
    spotify_id = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    uri = db.Column(db.String(128), nullable=False)
    href = db.Column(db.String(128), nullable=False)
    external_urls = db.Column(db.ARRAY(db.JSON))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def serialize(self, get_albums=True):
        if len(self.albums) > 0:
            latest_albums = sorted(self.albums, key=lambda album: album.created_at, reverse=True)
            latest_album = latest_albums[0].serialize(get_artists=False)
        else:
            latest_album = None
        artist_dict = {
            "id": self.id,
            "spotify_id": self.spotify_id,
            "name": self.name,
            "uri": self.uri,
            "href": self.href,
            "external_urls": self.external_urls,
            "latest_album": latest_album,
            "created_at": self.created_at.isoformat(),
        }
        if get_albums:
            artist_dict["albums"] = [album.serialize(get_artists=False) for album in self.albums]
        return artist_dict