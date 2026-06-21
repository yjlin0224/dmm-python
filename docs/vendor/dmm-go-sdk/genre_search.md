# Genre Search

<!-- markdownlint-disable MD010 -->

<https://github.com/dmmlabo/dmm-go-sdk/blob/f67870f8/api/genre.go#L11-L44>

```go
type GenreService struct {
	ApiID       string `mapstructure:"api_id"`
	AffiliateID string `mapstructure:"affiliate_id"`
	FloorID     string `mapstructure:"floor_id"`
	Initial     string `mapstructure:"initial"`
	Length      int64  `mapstructure:"hits"`
	Offset      int64  `mapstructure:"offset"`
}

type GenreRawResponse struct {
	Request GenreService  `mapstructure:"request"`
	Result  GenreResponse `mapstructure:"result"`
}

type GenreResponse struct {
	ResultCount   int64   `mapstructure:"result_count"`
	TotalCount    int64   `mapstructure:"total_count"`
	FirstPosition int64   `mapstructure:"first_position"`
	SiteName      string  `mapstructure:"site_name"`
	SiteCode      string  `mapstructure:"site_code"`
	ServiceName   string  `mapstructure:"service_name"`
	ServiceCode   string  `mapstructure:"service_code"`
	FloorID       string  `mapstructure:"floor_id"`
	FloorName     string  `mapstructure:"floor_name"`
	FloorCode     string  `mapstructure:"floor_code"`
	GenreList     []Genre `mapstructure:"genre"`
}

type Genre struct {
	GenreID string `mapstructure:"genre_id"`
	Name    string `mapstructure:"name"`
	Ruby    string `mapstructure:"ruby"`
	ListURL string `mapstructure:"list_url"`
}
```
