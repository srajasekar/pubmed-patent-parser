-- pubmed_Article(Id, Abstract, Body)
create table pubmed_Article(
    Id integer not null auto_increment,
    ArticleId long varchar,
    ArticleKeywords long varchar,
    Abstract long varchar,
    Body long varchar,
    PubDate Date,
    constraint ARTPK1 primary key(Id)
);

-- pubmed_Id(ArtilceId, PubIdType, PubId)
create table pubmed_Id (
    ArtilceId integer not null,
    PubIdType varchar(32),
    PubId varchar(32),
    constraint IDFK1 foreign key(ArtilceId) references pubmed_Article(Id)
);

-- pubmed_Title(ArtilceId, Title)
create table pubmed_Title (
    ArticleId integer not null,
    Title long varchar,
    constraint TITFK1 foreign key(ArticleId) references pubmed_Article(Id)
);

-- pubmed_Contributor(ArtilceId, ContribType, Surname, GivenNames)
create table pubmed_Contributor (
    ArtilceId integer not null,
    ContribType varchar(32),
    Surname varchar(256),
    GivenNames varchar(256),
    constraint CONTRIBFK1 foreign key(ArtilceId) references pubmed_Article(Id)
);

-- pubmed_Keyword(ArtilceId, Keyword)
create table pubmed_Keyword (
    ArtilceId integer not null,
    Keyword varchar(256),
    constraint KWFK1 foreign key(ArtilceId) references pubmed_Article(Id)
);

-- pubmed_Reference(Id, AricleId, RefId, RefType, Source, Title, PubYear, PubIdType, PubId)
create table pubmed_Reference (
    Id integer not null auto_increment,
    ArticleId integer not null,    
    RefId varchar(32),
    RefType varchar(32),
    Source varchar(256),
    Title long varchar,
    PubYear integer,
    PubIdType varchar(32),
    PubId varchar(32),
    constraint REFPK1 primary key(Id),
    constraint REFFK1 foreign key(ArticleId) references pubmed_Article(Id)
);

-- pubmed_RefContributor(Id, ContribType, Surname, GivenNames)
create table pubmed_RefContributor (
    RefId integer not null,
    ContribType varchar(32),
    Surname varchar(256),
    GivenNames varchar(256),
    constraint REFCONTRIBFK1 foreign key(RefId) references pubmed_Reference(Id)
);