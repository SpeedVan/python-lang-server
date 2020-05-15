package main

import (
	"github.com/SpeedVan/go-common/app/web"
	"github.com/SpeedVan/go-common/config/env"
	"github.com/SpeedVan/go-common/log"
)

func main() {
	if cfg, err := env.LoadAllWithoutPrefix("SCHEDULER_"); err == nil {
		logger := log.NewCommon(log.Debug)
		app := web.New(cfg, logger)
		// app.HandleController(controller.New(list))
		// app.RegisterOnShutdown(c.SubStopFunc)
		app.Run(log.Debug)
	}
}
