# Floor List

<!-- markdownlint-disable MD010 -->

<https://github.com/dmmlabo/dmm-go-sdk/blob/f67870f8/api/floor.go#L10-L40>

```go
type FloorService struct {
	ApiID       string `mapstructure:"api_id"`
	AffiliateID string `mapstructure:"affiliate_id"`
}

type FloorRawResponse struct {
	Request FloorService  `mapstructure:"request"`
	Result  FloorResponse `mapstructure:"result"`
}

type FloorResponse struct {
	Site []Site
}

type Site struct {
	Name     string       `mapstructure:"name"`
	Code     string       `mapstructure:"code"`
	Services []DMMService `mapstructure:"service"`
}

type DMMService struct {
	Name   string     `mapstructure:"name"`
	Code   string     `mapstructure:"code"`
	Floors []DMMFloor `mapstructure:"floor"`
}

type DMMFloor struct {
	ID   int64  `mapstructure:"id"`
	Name string `mapstructure:"name"`
	Code string `mapstructure:"code"`
}
```
