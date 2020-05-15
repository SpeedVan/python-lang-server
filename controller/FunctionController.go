package controller

import (
	"net/http"
	"sync"

	"github.com/SpeedVan/go-common/app/rest"
	"github.com/gorilla/mux"
)

// LangServerControllerBeta todo
type LangServerControllerBeta struct {
	rest.Controller
	Cache *sync.Map
}

// NewLangServerControllerBeta todo
func NewLangServerControllerBeta() *LangServerControllerBeta {

	return &LangServerControllerBeta{
		Cache: &sync.Map{},
	}
}

// GetRoute todo
func (s *LangServerControllerBeta) GetRoute() rest.RouteMap {
	items := []*rest.RouteItem{
		{Path: "/do/{sessionID}", HandleFunc: s.Do},
	}

	return rest.NewRouteMap(items...)
}

// Do todo
func (s *LangServerControllerBeta) Do(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	sessionID := vars["sessionID"]
	if _, exist := s.Cache.Load(sessionID); exist {

	}
}
